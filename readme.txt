* light weight/open sources databases like sqlite/hsql/mysql/postgres
	Able to use verz simply and in all os platforms (also very small docker)

* Naming convension of tables and columns is better to be underscore_name

cURL:
---
DIT/Unit/List
    curl -i -X GET 'http://127.0.0.1:5000/unit'
DIT/Unit/add
    curl -i -X POST \
       -H "Content-Type:application/json" \
       -d \
    '{  "abbreviated_name": "Lt"}' \
     'http://127.0.0.1:5000/unit/Liter'
DIT/Unit/delete
    curl -i -X DELETE \
    'http://127.0.0.1:5000/unit/Kilogeram13'
DIT/Unit/update
    curl -i -X PATCH \
       -H "Content-Type:application/json" \
       -d \
    '{"abbreviated_name": "Kg20"}' \
     'http://127.0.0.1:5000/unit/Kilogeram2'
---
DIT/Category/list
    curl -i -X GET \
    'http://127.0.0.1:5000/category'
DIT/Category/list-filter
    curl -i -X GET \
     'http://127.0.0.1:5000/category?PricingMethod=PM2'
DIT/Category/list-pagination
    curl -i -X GET \
   -H "pageSize:3" \
   -H "page:2" \
   -H "orderBy:Name desc" \
    'http://127.0.0.1:5000/category'
DIT/Category/add
    curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
    '{"Code": "6","PricingMethod": "PM2"}' \
     'http://127.0.0.1:5000/category/Cat6'
DIT/Category/delete
    curl -i -X DELETE \
 'http://127.0.0.1:5000/category/Cat6'
DIT/Category/update
    curl -i -X PATCH \
   -H "Content-Type:application/json" \
   -d \
    '{"Code": "50","PricingMethod": "PM11"}' \
     'http://127.0.0.1:5000/category/Cat5'
--
DIT/Partstore/list
   curl -i -X GET \
     'http://127.0.0.1:5000/partstore'
DIT/Partstore/list-filter
    curl -i -X GET \
     'http://127.0.0.1:5000/partstore?PartRef=2&StoreRef=2'
DIT/Partstore/list-pagination
    curl -i -X GET \
   -H "pageSize:10" \
   -H "page:1" \
   -H "orderBy:PartRef desc, StoreRef asc" \
     'http://127.0.0.1:5000/partstore'
DIT/Partstore/add
    curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
    '{"PartRef": 1,
            "StoreRef": 1,
            "PositionRef": 1,
            "State": "State1"
        }' \
     'http://127.0.0.1:5000/partstore'
DIT/Partstore/delete
    curl -i -X DELETE \
     'http://127.0.0.1:5000/partstore/10'
DIT/Partstore/update
    curl -i -X PATCH \
   -H "Content-Type:application/json" \
   -d \
    '{ "PartRef": 9, "StoreRef": 2, "PositionRef": 1, "State": "State1"}' \
     'http://127.0.0.1:5000/partstore/9'
