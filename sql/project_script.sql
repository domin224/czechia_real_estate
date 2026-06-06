-- Adding region and district code columns to the real estate table
alter table czechia_real_estate
add column "region_code" text,
add column "district_code" text;

-- Filling region_code (first 5 characters) and district_code (first 6 characters) from the NUTS_LAU code
update czechia_real_estate
set
    region_code = left(nuts_lau, 5),
    district_code = left(nuts_lau, 6);

-- Adding columns for price per square meter of house and land
alter table czechia_real_estate 
add column "price_per_m2_house" int,
add column "price_per_m2_land" int;

-- Calculating price per m2 for house and land where size is known and not zero
update czechia_real_estate
set
    price_per_m2_house = case 
        when house_size_m2 is not null and house_size_m2 != 0 
        then price_czk / house_size_m2 
        else null 
    end,
    price_per_m2_land = case 
        when land_size_m2 is not null and land_size_m2 != 0 
        then price_czk / land_size_m2 
        else null 
    end;

-- Listing average apartment prices per region and disposition, sorted by disposition (ascending) and price (descending)
select
    cr.name,
    ac.disposition,
    round(avg(cre.price_czk), 0) as avg_price,
    ac.code
from czechia_real_estate cre
left join czechia_region cr 
    on cre.region_code = cr.code
left join apartment_category ac 
    on cre.disposition = ac.code
where cr.name is not null
group by cr.name, ac.disposition, ac.code
order by ac.disposition, avg_price desc;

-- Calculating average price per m2 for houses and land by district
select
	cd.name,
	round(avg(cre.price_per_m2_house), 0) as avg_house_price_per_m2,
    round(avg(cre.price_per_m2_land), 0) as avg_land_price_per_m2,
    round(avg(cre.price_czk), 0) as avg_price
from czechia_real_estate cre
left join czechia_district cd
	on cre.district_code = cd.code
where
	cre.house_size_m2 is not null and 
	cre.land_size_m2 is not null and
	cd.name is not null
group by cd.name
order by avg_house_price_per_m2 desc;

-- Creating a table for payroll data by region
create table czechia_payroll (
    region_code varchar(10) not null,
    payroll bigint not null,
    payroll_men bigint not null,
    payroll_women bigint not null,
    med_payroll bigint not null,
    med_payroll_men bigint not null,
    med_payroll_women bigint not null
);

-- Selecting average house price and payroll data per region
select
	cre.region_code,
	avg(cre.price_czk) as avg_price,
	cp.payroll,
	cp.payroll_men,
	cp.payroll_women
from czechia_real_estate cre
left join czechia_payroll cp on cre.region_code = cp.region_code
where cre.region_code <> ''
group by cre.region_code, cp.payroll, cp.payroll_men, cp.payroll_women;

-- Creating a table showing how many years of income are needed to afford an average house in each region
create table payroll_to_home as
select
    cre.region_code,
    round(avg(cre.price_czk) / (cp.payroll * 12.0), 2) as years_total,
    round(avg(cre.price_czk) / (cp.payroll_men * 12.0), 2) as years_men,
    round(avg(cre.price_czk) / (cp.payroll_women * 12.0), 2) as years_women
from
    czechia_real_estate cre
left join
    czechia_payroll cp on cre.region_code = cp.region_code
where
    cre.region_code <> ''
group by
    cre.region_code,
    cp.payroll,
    cp.payroll_men,
    cp.payroll_women;

-- Creating a cleaned version of the historic real estate price table with region and district codes
create table clean_historic_prices as
select 
	h.category_main,
	h.year,
	h.avg_price,
	cd.code as district_code,
	cr.code as region_code
from historic_real_estate h
left join czechia_district cd on h.region = cd.name
left join czechia_region cr on h.region = cr.name;

-- Updating missing region_code values using the first 5 characters of district_code
update clean_historic_prices
set region_code = left(district_code, 5)
where district_code is not null and district_code <> '';

-- Removing rows without valid district_code
delete from clean_historic_prices
where district_code is null or district_code = '';

-- Inserting average house prices per district and region for 2025 into the historic price table
insert into clean_historic_prices (category_main, year, avg_price, district_code, region_code)
select 
    category_main_cb, 
    2025 as year, 
    avg(price_per_m2_house) as avg_price, 
    district_code, 
    region_code
from 
    czechia_real_estate
where 
    date_parsed::date >= '2025-01-01' and date_parsed::date < '2026-01-01'
group by 
    category_main_cb, district_code, region_code;

-- Inserting missing historic data for Prague with manually assigned codes
insert into clean_historic_prices (category_main, year, avg_price, district_code, region_code)
select category_main, year, avg_price, 'CZ0100', 'CZ010'
from historic_real_estate
where region = 'Hlavní město Praha';

 
 



