{{
    config(
        materialized='view'
    )
}}


with 

tripdata as (

    select * from {{ source('staging', 'fhv_tripdata')}}
    where EXTRACT(YEAR from pickup_datetime) = 2019
),

renamed as (

    select *

    from tripdata

)

select * from renamed


-- dbt build --select stg_fhv_tripdata --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
