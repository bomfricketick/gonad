{%- macro create_db(database) -%}
IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE [name] = N'{{ database }}')
    CREATE DATABASE {{ database }};
{%- endmacro -%}


{%- macro use_db(database) -%}
USE {{ database}};
{%- endmacro -%}


{%- macro create_test_results_table() -%}
IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE [name] = N'test_result' AND [type] = N'U')
    CREATE TABLE [dbo].[test_result] (
        id int IDENTITY(1,1) NOT NULL
        ,test_name varchar(50) NOT NULL
        ,test_date date NOT NULL
        ,test_time time NOT NULL
        ,targeted_tbl varchar(50) NOT NULL
        ,depenant_tbl varchar(50) NOT NULL
        ,test_status varchar(50) NOT NULL
        ,test_result decimal(10,2) NOT NULL
        ,sql varchar(max) NOT NULL
    );
{%- endmacro -%}


{%- macro create_profiling_table() -%}
IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE [name] = N'profiling' AND [type] = N'U')
    CREATE TABLE [dbo].[profiling] (
        id int IDENTITY(1,1) NOT NULL
        ,schema_name varchar(50) NOT NULL
        ,table_name varchar(50) NOT NULL
        ,column_name varchar(50) NOT NULL
        ,row_count int NULL
        ,not_null_proportion decimal(10,2) NULL
        ,distinct_proportion decimal(10,2) NULL
        ,dictinct_count int NULL
        ,is_unique bit NULL
        ,min_value varchar(50) NULL
        ,max_value varchar(50) NULL
        ,avg_value decimal(10,2) NULL
        ,profiled_at datetime NULL
        ,std_dev_population decimal(10,2) NULL
        ,std_dev_sample decimal(10,2) NULL
        ,_column_position int NULL
    );
{%- endmacro -%}
