import os
import requests
import pandas as pd
import time
import re
from tqdm import tqdm
from datetime import date

class RealityScraper:

    def __init__(self):
        self.base_url = "https://www.sreality.cz/api/cs/v2/estates"
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json',
            'Accept-Language': 'cs-CZ,cs;q=0.9',
            'Referer': 'https://www.sreality.cz/'
        }

    def extract_sizes(self, name, category_main_cb):
        """
        Extrahuje velikost nemovitosti a dispozici podle typu nemovitosti.
        """
        size_match = re.findall(r'(\d+)\s*m²', name)
        disposition_match = re.search(r'(\d\+\w+)', name)
        comment_match = re.search(r'\(([^)]+)\)', name)

        comment = comment_match.group(1) if comment_match else None

        # Mapa pro kódování dispozice
        disposition_mapping = {
            '1+kk': 1,
            '1+1': 2,
            '2+kk': 3,
            '2+1': 4,
            '3+kk': 5,
            '3+1': 6,
            '4+kk': 7,
            '4+1': 8,
            '5+kk': 9,
            '5+1': 10
        }

        disposition_code = None
        if disposition_match:
            disposition_str = disposition_match.group(1)
            disposition_code = disposition_mapping.get(disposition_str)

        if category_main_cb == 2:  # Domy
            return {
                'house_size_m2': int(size_match[0]) if len(size_match) >= 1 else None,
                'land_size_m2': int(size_match[1]) if len(size_match) >= 2 else None,
                'disposition': disposition_code,
                'comment': comment
            }
        else:  # Byty
            return {
                'house_size_m2': int(size_match[0]) if size_match else None,
                'land_size_m2': None,
                'disposition': disposition_code,
                'comment': comment
            }

    def parse_estate(self, estate):
        try:
            seo = estate.get('seo', {})
            category_main_cb = seo.get('category_main_cb')
            category_type_cb = seo.get('category_type_cb')
            category_sub_cb = seo.get('category_sub_cb')
            full_locality = seo.get('locality')

            if category_type_cb != 1:
                return None
            if category_main_cb not in [1, 2]:  # Pouze byty a domy
                return None
            if estate.get('price') == 1:
                return None

            parsed = {
                'hash_id': estate.get('hash_id'),
                'name': estate.get('name', 'Unnamed'),
                'price_czk': estate.get('price'),
                'date_parsed': date.today().isoformat(),
                'is_auction': estate.get('is_auction', False),
                'latitude': estate.get('gps', {}).get('lat'),
                'longitude': estate.get('gps', {}).get('lon'),
                'category_main_cb': category_main_cb,
            }

            # Přidej category_sub_cb pouze pro domy
            if category_main_cb == 2:
                parsed['category_sub_cb'] = category_sub_cb

            parsed.update(self.extract_sizes(parsed['name'], category_main_cb))

            labels_all = estate.get('labelsAll', [])
            flattened = [label for sub in labels_all for label in sub]

            parsed.update({
                'new_building': 'new_building' in flattened,
                'after_reconstruction': 'after_reconstruction' in flattened,
                'furnished': 'furnished' in flattened,
                'partly_furnished': 'partly_furnished' in flattened,
                'not_furnished': 'not_furnished' in flattened,
                'in_construction': 'in_construction' in flattened
            })

            return parsed
        except Exception as e:
            print(f"Error parsing estate: {e}")
            return None

    def fetch_estates(self, page=1, per_page=500):
        try:
            response = requests.get(self.base_url, params={
                'category_type_cb': 1,  # Prodej
                'page': page,
                'per_page': per_page
            }, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            estates = []
            for e in data.get('_embedded', {}).get('estates', []):
                parsed = self.parse_estate(e)
                if parsed:
                    estates.append(parsed)

            return pd.DataFrame(estates)
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            return pd.DataFrame()

    def scrape_all_pages(self, max_pages=1):
        all_data = []
        for page in range(1, max_pages + 1):
            print(f"Fetching page {page}...")
            df = self.fetch_estates(page=page)
            if df.empty:
                break
            all_data.append(df)
            time.sleep(0.5)
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

    def remove_duplicates(self, df, hash_id_column='hash_id'):
        """
        Odstraní duplicitní záznamy podle hash_id.
        """
        if df.empty:
            return df
            
        if hash_id_column not in df.columns:
            print(f"Chyba: Sloupec '{hash_id_column}' nebyl nalezen v CSV souboru.")
            print(f"Dostupné sloupce: {list(df.columns)}")
            return df
        
        # Počet řádků před odstraněním duplicit
        total_rows_before = len(df)
        
        # Odstranění duplicit podle hash_id (ponechá první výskyt)
        df_no_duplicates = df.drop_duplicates(subset=[hash_id_column], keep='first')
        
        # Počet řádků po odstranění duplicit
        total_rows_after = len(df_no_duplicates)
        
        # Počet odstraněných duplicit
        duplicates_removed = total_rows_before - total_rows_after
        
        print(f"Odstraněno {duplicates_removed} duplicitních záznamů.")
        print(f"Počet řádků po odstranění duplicit: {total_rows_after}")
        
        return df_no_duplicates

    def save_to_csv(self, df, filename):
        if df.empty:
            print("No data to save.")
            return
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Saved {len(df)} estates to {filename}")

    def main(self, max_pages=1):
        print("Downloading all estates...")
        full_df = self.scrape_all_pages(max_pages=max_pages)
        if full_df.empty:
            print("No estates found.")
            return

        # Načtení starého CSV, pokud existuje
        old_df = pd.DataFrame()
        if os.path.exists('reality_houses.csv'):
            try:
                old_df = pd.read_csv('reality_houses.csv', dtype={'hash_id': str})
                print(f"Načteno {len(old_df)} existujících záznamů.")
            except Exception as e:
                print(f"Failed to load original CSV: {e}")

        # Spojení starých a nových dat
        if not old_df.empty:
            combined_df = pd.concat([old_df, full_df], ignore_index=True)
            print(f"Celkem {len(combined_df)} záznamů po spojení.")
        else:
            combined_df = full_df
            print(f"Použito {len(combined_df)} nových záznamů.")

        # Odstranění duplicit
        print("\nOdstraňuji duplicitní záznamy...")
        final_df = self.remove_duplicates(combined_df, 'hash_id')

        # Uložení do reality_houses.csv
        self.save_to_csv(final_df, 'reality_houses.csv')


if __name__ == "__main__":
    scraper = RealityScraper()
    scraper.main(max_pages=100)

