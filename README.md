
# Averigo16


## averigo_product_import
### Model : product.import
file : Binary : 
File_type : Selection : default

## base_averigo
### Model : customer.contract
name : Char : required
active : Boolean : default
partner_id: Many2one : tracking,check_company
date_start : Date : required,default,help
date_end : Date : help
advantages : Text : 
state  : Selection : group_expand,copy,tracking,default
company_id : Many2one: default,required
kanban_state : Selection: default,tracking,copy
currency_id :Many2one : related,readonly

### Model : res.customer.type
customer_type_id :Char: size,required
customer_name_id : char: required

### Model : hr.employee
first_name : Char : tracking
last_name : Char : tracking
employee_code: Char : 
division_id : Many2one : 
street : Char : related,readonly,store
street2 : Char : related,readonly,store
city  : Char : related,readonly,store
zip : Char: related,readonly,store
state_id : Many2one: related,readonly,store

### Model : res.app.users
name : Char : required
active : Boolean : default

email : Char : required
mobile : Char : 
zip : Char : 
phone : Char : size
street : Char : 
city : Char : 
county : Char : 
state_id : Many2one : 
country_id : Many2one : 
end_user : Boolean : default
code : Char : 
devicetoken : Char : 
last_session_id : Many2one : 
last_session_date : Datetime : related
lastname : Char : 
device_udid : Char : 
nickname : Char : 
product_related_mailid : Char : 
enable_sms : Selection : default
enabel_newsletter : Selection : default
password : Char : 
app_related_mailid : Char : 
item_reconcile : Selection : default
usertype : Selection : default
service_name : Char : 
companyacro : Char : 
adminemaillist : Char : 
company_name : Char : 
profile_image : Boolean : 
item_receive : Selection : default
item_add : Selection : default
otp : Integer : 
password_reset_request : Boolean : default
devicetype : Char : 
last_visted : Many2one : 
is_imported : Boolean : default

### Model : app.user.pwd.reset
app_user_id : Many2one : required
user_name : Char : default: related
user_email : Char : default: related
new_password : Char : 
confirm_pwd : Char : 
check_match : Boolean : 

### Model : res.company
state_id : Many2one : inverse
county : Char : 
zip : Char : size
active : Boolean : default
report_logo : Binary : 
support_email : Char : 
legal_name : Char : 
language : Many2one : required
decimal_precision : Integer : default,digits
date_format : Char : 
time_format : Char : 
is_main_company : Boolean : default
department_ids : One2many : 
division_ids : One2many : 
enable_item_code : Boolean : 
operator_domain : Char : 
base_domain : Char : 
exact_domain : Char :
date_format : Char : 
date_format_selection : Selection : 
time_format_selection : Selection : default
shipping_zip : Char : size
shipping_street : Char : default
shipping_street2 : Char : default
shipping_city : Char : default
shipping_county : Char : default
shipping_state_id : Char : default
shipping_country_id : Many2one : store
preview_date : Date : 
loaded_coa : Boolean : 

### Model : res.division
name : Char : required
company_id : Many2one : required,default
active : Boolean : default
zip : Char : size
street : Char :
street2 : Char : 
city : Char : 
county : Char : 
state_id : Many2one :
country_id : Many2one : 
division_address : Char : 
primary_division : Boolean : 

### Model : partner.delete.wizard
partner_ids : Many2many : 

### Model : res.partner
name : Char : index,size
kam : Many2one : 
is_customer : Boolean : 
open_order_count : Integer : 
code : Char :copy

operator_id : Many2one : default
address : Char : 
county : Char : 
zip :Char: size

ship_via :Many2one:
nick_name :Char:size
parent_partner_id :Many2one:
parent_id :Many2one:domain
division :Many2one:
price_category :Selection:
is_taxable :Boolean:
customer_type :Many2many:
in_service_date :Date:default
out_service_date :Date:
monthly_statement :Boolean:
master_invoice :Boolean:
group_master_invoice :Selection:
fuel_charge :Boolean:
hazard_fee :Boolean:
out_reason :Text:
special_notes :Tex:
contract_id :Many2one:
contract_warning :Boolean: store=True,groups
contracts_count :Integer:
is_primary :Boolean: default
duplicate_primary :Boolean:
subsidy :Boolean:
subsidy_amount :Float:
subsidy_percentage :Float:
po_check :Boolean:
po_no :Char:
activities_count :Integer:
nick_name_view :Char:
primary_contact_id :Many2one:

### Model : ship.via
name :Char:required
operator_id :Many2one:index,default

### Model : res.users
user_type :Selection:default
first_name :Char:
last_name :Char:
role_selection :Selection:
login :Char:required:
group_micro_market :Boolean:default
allow_all_mm :Boolean: default=True
group_micro_market_access :Many2many:
group_user_management :Boolean:default
group_user_management_access :Many2many:
group_gpm :Boolean:default
group_gpm_access :Many2many:
group_home_screen_image :Boolean:default
group_home_screen_image_access :Many2many:
group_portal_user :Boolean:default
group_portal_user_access :Many2many:
group_reports :Boolean:default
group_reports_access :Many2many:default
group_operators :Boolean:default
group_operators_access :Many2many:
operator_ids :Many2many:
company_domain :Char:
micro_market_ids :Many2many:
group_company_info :Boolean:
notification_type :Selection:required, default
group_inventory :Boolean:default
group_hr :Boolean:default
group_customer_care :Boolean:default
group_users :Boolean:default
group_division :Boolean:default
group_contract :Boolean:default
group_operator_report :Boolean:default
menu_id :Many2one:
menu_ids :Many2many:

### Model : access.permissions
name :Char:required

### Model : uom.uom
company_id:Many2one:default

### Model : user.session.history
sequence :Char:
user_id :Many2one:
operator_id :Many2one:
location_id :Many2one:
micro_market_id :Many2one:
session_date :Datetime:
purchase_qty :Integer:
purchase_value :Float:
product_list :One2many:
move_id :Many2one:
tax_amount :Float:
crv_tax :Float:
payment_method :Char:
card_last :Char:
total_trans_amount :Float:
total_crv_amount :Float:
total_sales_amount :Float:
uniqueidentifier :Char:
room_no :Char:
membership_number :Char:
hosttransactionid :Char:
processstatus :Char:
cash_amount :Float:

### Model : session.product.list
company_id:Many2one:default
session_id :Many2one:
product_id :Many2one:
qty :Integer:
product_uom_id :Many2one: readonly
price :Float:
net_price :Float:
tax_amount :Float:
crv_tax :Float:
featured :Char:
list_price :Float:
special :Char:
user_type :Char:

### Model : zip.county
zip :Char:
city :Char:
state :Char:
county :Char:
area_codes :Char:
country :Char:
latitude :Float:
longitude :Float:


## averigo_create_not_exist
### Model : import.fail.log
user :Many2one:default
attempt_id :Char:
company_id :Many2one:default
entity :Char:
success :Integer:



## averigo_employee_user
### Model : hr.employee
purchase_limit :Float:
is_manager :Boolean:

### Model : hr.employee.public
first_name :Char:
last_name :Char:


## averigo_mail_templates
### Model : mail.template
company_id :Many2one:required,default
active :Boolean: default
default :Boolean:
check_company :Boolean:


## averigo_marketing_campaign
### Model : mail.blacklist
company_id :Many2one: default

### Model : mailing.contact
company_id :Many2one:default

### Model : mailing.list
company_id :Many2one:default

### Model : mailing.mailing
company_id :Many2one:default
campaign_id :Many2one:
subject :Char:required, translate

### Model : res.users
group_mail_marketing :Boolean:default

### Model : utm.campaign
name :Char: required,translate
company_id :Many2one:default
active :Boolean: default
parent_id :Many2one:
user_id :Many2one:required,default
start_date :Date:default
end_date :Date:
type_id :Many2one:
currency_id :Many2one:related
campaign_budget :Monetary:default,currency_field
campaign_spent :Monetary: default,currency_field
campaign_expect :Monetary: default,currency_field
description :Text:size

### Model : utm.mixin
source_id :Many2one:

### Model : utm.source
name :Char: required,translate

### Model : utm.stage'
company_id :Many2one:default

### Model : utm.tag
company_id :Many2one:default



## averigo_misc
### Model :res.customer.type
color :Char:

### Model :res.months
name :Char:
code :Char:
number :Integer:


## averigo_product_opening_stock
### Model :product.template
opening_entry:Boolean:

### Model :popup.message
message :Text:

## sendgrid_email
### Model :email.sent
name :Char:required
email_id :Char:required
operator_id :Many2one:default

### Model :mail.template
temp_id :Char:
generation :Char: default,readonly
version_status :Selection:
sedgrid_readonly :Boolean:default

### Model :email.template
temp_name :Char:required
operator_id :Many2one:default
generation :Char:default,readonly
ver_name :Char:
ver_subject :Char:required
ver_editor :Selection: default
temp_cont :Html: translate,sanitize
temp_id :Char:
version_status :Selection:

### Model :ir.config_parameter
company_id :Many2one    

### Model :mailing.mailing
email_temp :Many2one:
temp_id :Char:
from_email :Many2one:
to_email_partner :Many2many:
to_email_partner_check :Boolean;
to_email_lead :Many2many:
to_email_lead_check :Boolean:
to_email_contact :Many2many:
to_email_contact_check :Boolean:
to_email_applicant :Many2many:
to_email_applicant_check :Boolean:
email_finder :Integer:
sent_count :Integer:
send_grid_check :Boolean:
temp_check :Boolean:

### Model :email.api
name :Char:
company_name :Char:
recipient_name :Char:
to_email :Char:
to_email_partner :Many2one:
to_email_partner_check :Boolean:
to_email_lead :Many2one:
to_email_lead_check :Boolean:
to_email_contact :Many2one:
to_email_contact_check :Boolean:
to_email_applicant :Many2one:
to_email_applicant_check :Boolean:
from_email :Many2one:
temp_type :Many2one:
temp_id :Char:
send_date :Datetime:readonly,default
error_msg :Text:readonly
error_check :Boolean:
state :Selection:readonly,default
bounce_msg :Text:
email_finder :Integer:

### Model :res.config.settings
send_grid_api_check :Boolean:
send_grid_api_value :Char:config_parameter


## single_product_master
### Model :product.template
enable_product_code :Boolean:

### Model :product.template
subsidy_check :Boolean:default
fuel_check :Boolean:default
hazard_check :Boolean:default

### Model :account.tax
crv :Boolean:

### Model :res.partner
purchase_manager :Many2one:
contact_fname :Char:
contact_lname :Char:
credit_limit :Float:
return_period :Integer:
days :Char:default
buy_all :Boolean:default
vendor_approve :Boolean:default
vendor_1099 :Boolean:default
customer_id :Char: default
federal_tax :Char:
check_memo :Text:

### Model :res.users
upc_code_multi :Boolean:default

### Model :upc.code.history
note :Char:
product_id :Many2one:
user_id :Many2one:
time :Datetime:

### Model :product.template
upc_change_history :One2many:
categ_id :Many2one:change_default,group_expand,required,tracking
product_type :Selection:default,required
primary_upc :Char:
upc_code :Many2one:
operator_id :Many2one:required,index,default
product_code :Char: tracking
default_code :Char:tracking
tax_status :Selection: default
list_price_1 :Float: digits,tracking
list_price_2 :Float: digits,tracking
list_price_3 :Float:digits,tracking
sale_acc :Many2one:tracking
vendor :Many2one: tracking
cost_price :Float:digits
cogs_acc :Many2one:tracking
inventory_acc :Many2one:tracking
res_location :Many2one:
primary_location :Many2one:
primary_location :Many2one:default
res_partner :Many2one:tracking
res_manufacturer :Many2one:
manufacturer :Text:tracking
product_uom_ids :One2many:copy,tracking
upc_ids :One2many:ondelete,tracking,track_visibility
get_barcode :Boolean:default
upc_codes :Many2many
litre_type :Selection:
fluid_ounce :Float: digits
multiple_uom :Boolean:default
is_container_tax :Boolean:default
mnp_id :Char:
stock_open :Float:tracking,digits
reorder_point :Integer: default,tracking
reorder_qty :Integer, default, tracking
min_qty :Integer:default,tracking
max_qty :Integer:default,tracking
rate_per_uint :Float,digits
get_upc_code :Boolean:default
is_sugar_tax :Boolean:default
is_container_deposit :Boolean:default
product_image_ids :One2many:copy
last_purchase_date :Date:
crv_tax :Many2one:domain,track_visibility
container_deposit_amount :Float:digits

type :Selection:default, required
standard_price :Float:copy=True,inverse,search,digits,groups

### Model :multiple.uom
uom_template_id :Many2one:index
convert_uom :Many2one:required
quantity :Integer:
standard_price :Float:digits
sale_price_1 :Float:digits
sale_price_2 :Float:digits
sale_price_3 :Float:digits


### Model :barcode.barcode
barcode :Char:
get_barcode :Boolean:default
upc_id :Many2one:

### Model :upc.code.multi
upc_code_id :Char:tracking
get_upc_code :Boolean:default
upc_id :Many2one:
product_company_id :Many2one:related
operator_id :Many2one:required,default

### Model :extra.image
name :Char:required
image_1920 :Image:required
product_tmple_id :Many2one:index,ondelete
sequence :Integer:default,index

### Model :stock.quant
warehouse_id :Many2one:inverse,domain
location_id:Many2one:domain,auto_join,ondelete,readonly,required,index,check_company
quantity :Float: readonly,digits
inventory_quantity:Float:inverse,groups=,digits
reserved_quantity :Float”default,readonly,required digits

### Model :create.products

upc_code :Many2one:
products_ids :Many2one:
upc_ids :One2many:
create_product_id :Many2many:
get_barcode :Boolean:default
res_location :Many2one:
primary_location :Many2one:default
type :Selection:default
product_code :Char:
name :Char:
standard_price :Float:
list_price_1 :Float:
operator_id :Many2one:required,index,default
categ_id :Many2one:default
container_tax :Many2one:
tax_status :Selection:default
image_1920 :Binary:
is_container_deposit :Boolean:default
upc_code_scan :Char:
uom_id :Many2one:default,required

### Model :create.bulk.products
product_ids :One2many:
operator_id :Many2one:required,index,default
name :Char:
scan_from_gpm :Boolean:default

## micro_market
### Model :additional.tax
name :Char:default
operator_id :Many2one:default
additional_tax_label_1 :Char:
additional_tax_label_2 :Char:
additional_tax_label_3 :Char:
tax_rate_1 :Float:
tax_rate_2 :Float:
tax_rate_3 :Float:

### Model :uuid.uuid

name :Char:
beacon_major :Char:required tracking, copy
beacon_minor :Char:required, tracking, copy
merchant_id :Char: tracking,copy
terminal_id :Char: tracking,copy
apriva_client_id :Char:tracking,copy
secret_key :Char:copy
secret_key_masked :Char:copy
micro_market_id :Many2one:domain
operator_id :Many2one:related
partner_id :Many2one:related
mask_secret_key :Boolean:

### Model :product.discontinue
partner_ids :Many2many:domain
partner_dom_ids :Many2many:
micro_market_ids :Many2many: domain
product_ids :Many2many
otal_markets :Integer:
total_products :Integer:

### Model :product.reverse.discontinue
product_id :Many2one:

### Model :location.tiers
name :Char:
field_id :Many2one:
view_id_tree :Many2one:
view_id_form :Many2one:

### Model :stock.warehouse
name :Char:index,required,default,tracking,size
partner_id :Many2one:default,check_company,ondelete,copy
partner_name :Char:store
code :Char:required,size
location_id :Char:size,tracking,copy
location_type :Selection:default,index,required,tracking
location_type_view :Selection:default,index,required,tracking,store,related
street :Char:
street2 :Char:
zip :Char:size
city :Char:
county :Char:
state_id :Many2one:domain
state_name :Char:store
country_id :Many2one:
email :Char:store,readonly
contact_person :Char:store,readonly
operator_own :Boolean:
uuid :Many2one:tracking,domain,copy
beacon_major :Char:tracking,copy,related
beacon_minor :Char:tracking,copy,related
merchant_id :Char:tracking,copy,related
terminal_id :Char:tracking,copy,related
apriva_client_id :Char:tracking,copy,related
secret_key :Char:copy,related
catalog_ids :Many2many:domain
select_catalog_products :Boolean:default
product_ids :Many2many:
single_product_ids :Many2many:
product_filter_ids :Many2many:store
catalog_product_ids :One2many:
market_product_ids :One2many:domain,tracking,copy
check_group :Boolean:
market_address :Char:
value :Float:
currency_id :Many2one:related
active_date :Date:default
low_stock :Integer:
avg_sale :Float: digits
total_sale :Float: digits
division_id :Many2one:
catalog_length :Integer:
operator_street :Char:related
operator_street2 :Char:related
operator_zip :Char:related
operator_county :Char:related
operator_city :Char:related
operator_state_id :Many2one:related
operator_country_id :Many2one:related
customer_street :Char:related
customer_street2 :Char:related
customer_zip :Char:related
customer_county :Char:related
customer_city :Char:related
customer_state_id :Many2one:related
customer_country_id :Many2one:related
have_shipping_customer :Boolean:store
partner_shipping_id :Many2one:
shipping_customer_street :Char:related
shipping_customer_street2 :Char:related
shipping_customer_zip :Char:related
shipping_customer_county :Char:related
shipping_customer_city :Char:related
shipping_customer_state_id :Many2one:related
shipping_customer_country_id :Many2one:related
longitude :Float:
latitude :Float:
image :Image:
image_128 :Image:related,max_width, max_height
catalogs_ids :Many2many:
internal_notes :Text:
special_notes :Text:tracking
current_date :Date:default
route :Many2one: tracking
frequency :Many2one: tracking,copy
tax :Many2one:
sales_tax :Float:digits, tracking
tax_warning :Text:
from_customer :Boolean:
last_ordered_warehouse :Many2one:
truck_driver :Many2one:
show_tax_warning :Boolean:
micro_market_products_count :Integer:
addl_tax :Boolean:
show_tax_rate_1 :Boolean:
show_tax_rate_2 :Boolean:
show_tax_rate_3 :Boolean:
tax_rate_1 :Float:
tax_rate_2 :Float:
tax_rate_3 :Float:
product_category_ids :Many2many:
dom_product_category_ids :Many2many:store
enable_tax_rate_1 :Boolean
enable_tax_rate_2 :Boolean
enable_tax_rate_3 :Boolean
partner_readonly :Boolean

### Model :product.micro.market
active :Boolean:related
product_id :Many2one:index,required,translate,domain,
add_upc :Char:
upc_ids :Many2many:tracking, store
name :Char:store, related
image :Image:related
image_32 :Image:related,max_height, max_width
image_64 :Image:related,max_height, max_width
catalog_id :Many2one:
product_code :Char:store,related
tax_status :Selection:tracking
categ_id :Many2one:store,related,index
list_price :Float:readonly,digits,tracking
subsidy :Float:digits, tracking
uom_category :Integer:
uom_id :Many2one:domain,tracking
micro_market_id :Many2one:index
max_qty :Integer:tracking,default
min_qty :Integer:tracking,default
description :Text:
state :Selection:store
price_status :Char:store
quantity :Float:digits
catalog_price :Float:digits
is_container_tax :Boolean:related
container_deposit_tax :Many2one:domain,tracking
container_deposit_amount :Float:digits
cost_price :Float:related, store,digits
discontinued :Boolean:default,store
eoq :Integer:
partner_id :Many2one:store,related,ondelete
company_id :Many2one:store,related
sales_tax :Float:store,related,digits
sales_tax_amount :Float:store,digits
discontinued_date :Date:
discontinued_user :Char:
opening_stock :Float:
is_discontinued :Boolean:
info :Text:
product_last_sales :Integer:store
tax_rate_percentage_1 :Float:
tax_rate_percentage_2 :Float:
tax_rate_percentage_3 :Float:
tax_rate_1 :Float:
tax_rate_2 :Float:
tax_rate_3 :Float:
enable_tax_rate_1 :Selection:default,tracking
enable_tax_rate_2 :Selection:default,tracking
enable_tax_rate_3 :Selection:default,tracking

### Model :catalog.micro.market
micro_market_id :Many2one:
catalog_id :Many2one:
product_id :Many2one:
select_product :Boolean:default
name :Char:
image :Image:
product_code :Char:
tax_status :Selection:
categ_id :Many2one:
list_price :Float: readonly,digits
upc_ids :Many2many:
uom_id :Many2one:
max_qty :Integer:
min_qty :Integer:

### Model :res.partner
total_mm :Integer:

### Model :product.market.uom
micro_market_id :Many2one:
product_id :Many2one:domain
uom_id :Many2one:
uom_ids :Many2many:
multiple_uom_ids :Many2many:
multiple_uom_id :Many2one:
add_product :Boolean:default
add_to_mm :Boolean:

### Model :account.move
micro_market_id :Many2one:domain

### Model :account.move.line
micro_market_id :Many2one:related, store
subsidy_amount :Float:digits

### Model :user.session.history
subsidy_amount :Float:digits

### Model :session.product.list
subsidy_amount :Float:

### Model :product.catalog
name :Char:required
active :Boolean:default
product_ids :Many2many:domain
product_filter_ids :Many2many:store
catalog_product_ids :One2many:copy
micro_market_ids :Many2many:
operator_id :Many2one:index,default,readonly
category_ids :Many2many:string
multiple_uom_products :One2many:
product_select_uom_length :Integer:store
catalog_type :Selection:default,required, tracking
show_wizard :Boolean:store
changed_catalog_ids :Many2many:

### Model :product.product
catalog_ids :Many2many:
catalog_filter_id :Many2one:
micro_market_id :Many2one:

### Model :product.product.catalog
product_id :Many2one:index, required,translate,domain
name :Char:
product_code :Char:
tax_status :Selection:
categ_id :Many2one:store, related
upc_ids :Many2many:tracking,store
image :Image:related
image_catalog :Image:max_width,max_height,related
list_price :Float: readonly,digits,tracking
uom_category :Integer:tracking
uom_ids :Many2many:store
catalog_id :Many2one:
description :Text:translate
specification :Text:translate
max_qty :Integer:tracking,default
min_qty :Integer:tracking,default


### Model :product.uom
catalog_id :Many2one:
product_id :Many2one:domain
uom_id :Many2one:
uom_ids :Many2many:
multiple_uom_ids :Many2many:
multiple_uom_id :Many2one:
add_product :Boolean:default
add_to_mm :Boolean:
micro_market_ids :Many2many:

### Model :stock.warehouse
pantry_product_ids :One2many:tracking,copy

### Model :product.pantry
pantry_id :Many2one:
active :Boolean:related
product_id :Many2one: index, required,domain,translate
add_upc :Char:
upc_ids :Many2many:tracking,store,
name :Char:
image :Image:related
image_32 :Image:related,, max_width,max_height
image_64 :Image:related,, max_width,max_height
catalog_id :Many2one:
product_code :Char:store,related
tax_status :Selection:tracking
categ_id :Many2one:store,related
list_price :Float:readonly,digits,tracking
uom_category :Integer:
uom_id :Many2one:domain,tracking
max_qty :Integer:tracking, default
min_qty :Integer:tracking, default
description :Text:
state :Selection:
price_status :Char:
quantity :Float:
catalog_price :Float:
select_product :Boolean:default
is_container_tax :Boolean:related
container_deposit_tax :Many2one:domain,related,tracking
cost_price :Float:related
partner_id :Many2one:store,related,ondelete
company_id :Many2one”store,related
sales_tax :Float:store, related
sales_tax_amount :Float:store
discontinued_date :Date:
discontinued_user :Char:

### Model :res.users
group_location :Boolean:default
group_vending :Boolean:default
group_store_order :Boolean:default
group_store_order_approval :default

### Model :route.route
name :Char:
desc :Char:
truck_id :Many2one:domain
warehouse_id :Many2one:domain
operator_id :Many2one:index,default,readonly

### Model :route.frequency
name :Char:
operator_id :Many2one:index,default,readonly,invisible
color :Char:

### Model :stock.location
warehouse_id :Many2one:
max_pallets :Integer:
height :Float:
width :Float:
depth :Float:
volume :Float:
is_bin_location :Boolean:

### Model :stock.picking
active :Boolean:default
micro_market_id :Many2one:domain
transit_location :Many2one:domain
transit_location_id :Many2one:states
warehouse_id :Many2one:domain
partner_id :Many2one:check_company,domain,states
scheduled_date :Datetime:inverse,store,index,default,tracking,states
promise_date :Date:default,states,tracking
company_id :Many2one:related,readonly,store,index
store_order_state :Selection:copy,index,readonly,store,tracking
picking_type_id :Many2one:required,readonly,states
priority :Selection:inverse,store,index,tracking,states
route :Many2one:states,tracking
order_date :Date:default,states,tracking
delivered_date :Date:copy
partner_address :Char:
total_quantity :Integer:
products :Integer:
reason_backorder :Text:
reason_backorder_note :Text:related
signature :Binary:copy,attachment
signed_by :Char: copy
signed_on :Date:copy
cus_signature :Binary:copy,attachment
cus_signed_by :Char:copy
cus_signed_on :Date:copy
store_order :Boolean:
partner_ids :Many2many:
add_all :Boolean:default,states
show_all :Boolean:states
category_ids :Many2many:states
category_dom_ids :Many2many:
transit_picking :Boolean:
transit_picking_id :Many2one:
return_picking :Boolean:
return_picking_id :Many2one:
pick_user_id :Many2one:
purchase_picking :Boolean:
order_number :Char:
receive_inventory :Boolean:
extra_mm_products_length :Integer:
dom_extra_mm_products :Many2many:
extra_mm_products :Many2many:
no_of_days :Integer:

### Model :stock.move
   source_stock :Integer:store
    dest_stock :Integer:store
    source_stock_uom :Char:
    dest_stock_uom :Char:
    max_qty :Integer:
    min_qty :Integer:
    categ_id :Many2one:store,related
    active :Boolean:default
    product_uom :Many2one:required,domain
    product_uom_ids :Many2many:
    product_last_sales :Integer
    micro_market_id :Many2one:
    ordered_qty :Integer:
    temp_qty :Float:
    product_code :Char:
    product_name :Char:
    select_product :Boolean:
    picking_qty :Integer:
    picked_qty :Integer:

### Model :stock.move.line
move_product_ids :Many2many:
picked_qty :Integer:
store_order :Boolean:store,related

### Model :res.config.settings
tax_cloud_id :Char: config_parameter
tax_cloud_key :Char:config_parameter

### Model :account.tax
micro_market_id :Many2one:copy

### Model :user.session.history
additional_tax_label_1 :Char:
additional_tax_rate_1 :Float:
additional_tax_label_2 :Char:
additional_tax_rate_2 :Float:
additional_tax_label_3 :Char:
additional_tax_rate_3 :Float:
micro_market_id :Many2one:index

### Model :session.product.list
additional_tax_amount_1 :Float:
additional_tax_amount_2 :Float:
additional_tax_amount_3 :Float:


## suspicious_login
### Model : res.users.activity
user_id :Many2one:
user_uid :Char:

### Model : res.users
otp :Char:

### Model :res.users.otp
user_id :Many2one:
otp :Char:

### Model :res.users.login.attempt
user_id :Many2one:
status :Selection:
failed_reason :Char:
location :Char:
ip_address :Char:
login_time :Datetime:
timezone :Char:
platform :Char:
browser :Text:


## averigo_material_transfer
### Model : stock.picking
material_transfer :Boolean:
issuer_id :Many2one:default,tracking
transfer_receiver_id :Many2one:tracking

### Model : stock.move
warehouse_dest_id :Many2one:domain
bin_dest_location :Many2one:domain
inventory_loc_stock :Integer:
transfer_loc_stock :Integer:


## averigo_accounting
### Model : account.account.type NOT USED IN ODOO16.IN ODOO 13 IT’S A M2O FIELD ,INSTEAD OF THIS MODEL USED A SELECTION FIELD FOR ACCOUNT TYPE,DEFINED ON account.account

### Model : account.move
bill_ids :Many2many:
is_misc_receipt :Boolean:
receipt_type :Selection:default,required
payment_amount :Float:
vendor_adv_balance :Float:
bank_name :Char:
authorisation_code :Char:
transaction_ref :Char:
check_ref :Char:
credit_card_ref :Char:
name_on_card :Char:
payer_name :Char:
payment_date :Date:
card_expiry_date :Date:
receipt_distribution_lines :One2many:
account_id :Many2one:
journal_id :Many2one:required,domain
payment_mode_id :Many2one:
payment_mode :Char:
check_id :Many2one:domain
compute_check_ids :Many2many:
total_container_deposit_view :Float:
total_sales_tax_amount_view :Float:
vendor_advance :Boolean:default
customer_advance :Boolean:default

### Model : account.move.line
advance :Boolean:
check_id :Many2one:
payment_mode_id :Many2one:

### Model : receipt.credit.distribution
account_id :Many2one:domain
amount :Float:
notes :Text:
move_id :Many2one:
company_id :Many2one:default
currency_id :Many2one:related

### Model : account.payment
customer_no :Char:related,states
vendor_no :Char:size,related,states
customer_debit :Char:copy
vendor_debit :Char:copy
partner_card_id :Many2one:states
check_id :Many2one:states
check_no :Char:
check_date :Date:
check_amount :Float:
check_bank_id :Many2one:
partner_bank_name :Char:
notes :Text:
internal_notes :Text:
revision_no :Integer:default
revision_date :Date:default
user_id :Many2one:readonly,default
advance_payment :Boolean:
payment_mode_id :Many2one:
check :Boolean:
balance_amount :Monetary:required,states,tracking
reconciled_misc_receipts_ids :Many2many:
has_misc_receipts :Boolean:
reconciled_misc_receipts_count :Integer:
advance_count :Integer:
bill_ids :One2many:
unapplied_amount :Float:
extra_unapplied_amount :Float:
narration :Text:
is_advance :Boolean:
is_bank :Boolean:
is_credit_card :Boolean:
is_write_off :Boolean:
invoice_balance :Float:
cust_advance_balance :Float:store
advance_move_line_ids :Many2many:store
phone :Char:related
division_id :Many2one:
bill_ids_len :Integer:
account_id :Many2one:tracking
account_dom_ids :Many2many:
credit_card_id :Many2one:states
card_type :Selection:default
card_number :Char:
card_name :Char:
card_expiry :Date:default

### Model : account.payment.mode
name :Char:required
type :Selection:required
operator_id :Many2one:default

### Model : bill.payment
name :Char:
partner_id :Many2one:
amount :Float:
payment_date :Date:default
state :Selection:default
operator_id :Many2one:default
user_id :Many2one:default
currency_id :Many2one:related
journal_id :Many2one:required,tracking,domain
payment_mode_id :Many2one('account.payment.mode',
account_id :Many2one:required,tracking
account_dom_ids :Many2many:
partner_bank_account_id :Many2one:domain
partner_bank_name :Char:
check_id :Many2one:
partner_card_id :Many2one:
card_type :Selection:default
card_number :Char:
vendor_advance_balance :Float:store
advance_move_line_ids :Many2many:store
bill_balance :Float:
phone :Char:related
bill_ids :One2many:related
bill_ids_len :Integer:
unapplied_amount :Float:
extra_unapplied_amount :Float:
narration :Text:
is_advance :Boolean:
is_bank :Boolean:
is_credit_card :Boolean:
is_check :Boolean:
is_write_off :Boolean:
check_no :Char:

### Model : bill.payment.lin
bill_payment_id :Many2one:
bill_id :Many2one:
operator_id :Many2one:related
currency_id :Many2one:related
name :Char:related
partner_id :Many2one:related
bill_date_due :Date:related
amount_total_view :Float:related
amount_adjusted :Float:
amount_residual :Float:
bill_amount_residual :Monetary:related
amount_residual_changed :Boolean:
advance_amount :Float:
amount_received :Float:
due_amount :Float:store
advance_move_line_id :Many2one:copy
have_advance_value :Boolean:
filter_advance_move_line_ids :Many2many:
unapplied_amount :Float:

### Model : default.payable
name :Char:default
operator_id :Many2one:default
payable_account_id :Many2one:domain
terms_discount_account_id :Many2one:domain
accrued_account_id :Many2one:domain
purchase_discount_account_id :Many2one:domain
insurance_account_id :Many2one:domain
misc_bill_account_id :Many2one:domain
advance_account_id :Many2one:domain
tax_account_id :Many2one:domain
ship_handling_account_id :Many2one:domain
write_off_account_id :Many2one:domain
bill_seq_id :Many2one:domain
bill_refund_seq_id :Many2one:domain
adv_payment_vendor_seq_id :Many2one:domain
payment_vendor_seq_id :Many2one:domain

### Model : default.receivable
name :Char:default
operator_id :Many2one:default
due_days :Integer:default,required
due_days_2 :Integer::default,required
due_days_3 :Integer::default,required
receivables_control_account_id :Many2one:domain
terms_discount_account_id :Many2one:domain
sales_tax_liability_account_id :Many2one:domain
s_h_account_id :Many2one:domain
accrued_receivable_account_id :Many2one:domain
rental_receivable_account_id :Many2one:domain
sugar_tax_account_id :Many2one:domain
hazard_fee_account_id :Many2one:domain
miscellaneous_receipt_control_account_id :Many2one:domain
sales_discount_account_id :Many2one:domain
advance_account_id :Many2one:domain
insurance_account_id :Many2one:domain
write_off_account_id :Many2one:domain
service_receivable_account_id :Many2one:domain
fuel_charge_account_id :Many2one:domain
inv_seq_id :Many2one:domain
inv_refund_seq_id :Many2one:domain
adv_payment_customer_seq_id :Many2one:domain
invoice_receipt_seq_id :Many2one:domain

### Model : general.ledger
name :Char:
restock_fee_credit_debit :Boolean:
restock_type :Selection:index,tracking
restock_fee_percent :Float:
restock_amount :Float:
display_account :Many2one:domain
service_charges :Many2one:domain
interest_earned :Many2one:domain
interest_paid :Many2one:domain
undeposited_funds :Many2one:domain
retained_earnings :Many2one:domain
journal_adjustment :Many2one:domain
restock_fee :Many2one:domain

### Model : invoice.receipt
name :Char:
partner_id :Many2one:
amount :Float:
receipt_date :Date:default
state :Selection:default
company_id :Many2one:default
user_id :Many2one:default
currency_id :Many2one:related
journal_id :Many2one:required,tracking,domain
payment_mode_id :Many2one:
account_id :Many2one:required,tracking
account_dom_ids :Many2many:
partner_bank_account_id :Many2one:domain
partner_bank_name :Char:
check_id :Many2one:
partner_card_id :Many2one:
card_type :Selection:default
card_number :Char:
cust_advance_balance :Float:store
advance_move_line_ids :Many2many:store
invoice_balance :Float:
phone :Char:related
invoice_ids :One2many:
invoice_ids_len :Integer:
unapplied_amount :Float:
extra_unapplied_amount :Float:
narration :Text:
is_advance :Boolean:
is_bank :Boolean:
is_credit_card :Boolean:
is_check :Boolean:
is_write_off :Boolean:
check_no :Char:

### Model : invoice.receipt.line
invoice_receipt_id :Many2one:
invoice_id :Many2one:
company_id :Many2one:related
currency_id :Many2one:related
name :Char:related
partner_id :Many2one:related
invoice_date_due :Date:related
amount_total_view :Float:related
amount_adjusted :Float:
amount_residual :Float:
invoice_amount_residual :Monetary:related
amount_residual_changed :Boolean:
advance_amount :Float:
amount_received :Float:
due_amount :Float:store
advance_move_line_id :Many2one:copy
have_advance_value :Boolean:
filter_advance_move_line_ids :Many2many:
unapplied_amount :Float:
from odoo import fields, models

### Model :ir.sequence
inv_seq :Boolean:default
inv_refund_seq :Boolean:default
bill_seq :Boolean:default
bill_refund_seq :Boolean:default
adv_payment_customer_seq :Boolean:default
adv_payment_vendor_seq :Boolean:default
payment_vendor_seq :Boolean:default
invoice_receipt_seq :Boolean:default
from odoo import fields, models

### Model :payment.bill.line
payment_id :Many2one:
invoice_id :Many2one:
company_id :Many2one:related
currency_id :Many2one:related
name :Char:related
partner_id :Many2one:related
invoice_date_due :Date:related
amount_total_view :Float:related
amount_adjusted :Float:
amount_residual :Float:
invoice_amount_residual :Monetary:related
amount_residual_changed :Boolean:
advance_amount :Float:
amount_received :Float:
due_amount :Float:store
advance_move_line_id :Many2one:copy
have_advance_value :Boolean:
filter_advance_move_line_ids :Many2many:
unapplied_amount :Float:

### Model :res.partner
property_account_receivable_id :Many2one:required,domain
control_account_id :Many2one:domain
sales_discount_account_id :Many2one:domain
advance_account_id :Many2one:domain
insurance_account_id :Many2one:domain
sales_tax_liability_account_id :Many2one:domain
terms_discount_account_id :Many2one:domain
shipping_handling_account_id :Many2one:domain
card_ids :One2many:
check_ids :One2many:

### Model :res.partner.bank
is_vendor :Boolean:
is_customer :Boolean:

### Model :res.partner.card
bank_id :Many2one:
card_type :Selection:default
card_number :Char:required
card_name :Char(:required
card_expiry :Date:required,default
sequence :Integer:default
partner_id :Many2one:ondelete,index,domain
company_id :Many2one:default,ondelete
is_vendor :Boolean:
is_customer :Boolean:

### Model :res.partner.check
check_bank_id :Many2one:
check_bank_account_id :Many2one:
check_number :Char:required
check_date :Date:required,default
check_amount :Float:digits
sequence :Integer:default
partner_id :Many2one:ondelete,index,domain
company_id :Many2one:default,ondelete
is_vendor :Boolean:
is_customer :Boolean:
is_advance :Boolean:

## overage_shrinkage_spoilage_report
### Model : overage.report
name = fields.Char:default
customer_ids = fields.Many2many:domain
partner_ids = fields.Many2many:
mm_dom_ids = fields.Many2many:
mm_ids = fields.Many2many:
category_ids = fields.Many2many:
search_string = fields.Char:
from_date = fields.Date:
to_date = fields.Date:
changes = fields.Many2many:domain
total_cost = fields.Float:
total_price = fields.Float:
total_quantity = fields.Integer:
record_count = fields.Integer:
company_id = fields.Many2one:default
division_ids = fields.Many2many:
dom_division_ids = fields.Many2many:
currency_id = fields.Many2one:related
line_ids = fields.One2many:
state = fields.Selection:default
product_ids = fields.Many2many:
product_dom_ids = fields.Many2many:
report_type = fields.Selection:default

### Model : overage.report.lines
mm_id = fields.Many2one:
user_id = fields.Many2one:
date = fields.Date:
product_id = fields.Many2one:
item_code = fields.Char:related,store
item_description = fields.Text:related
category_id = fields.Many2one:related,store
change_type = fields.Selection:
qty = fields.Integer:
company_id = fields.Many2one:default
currency_id = fields.Many2one:related
cost = fields.Float:
total_cost = fields.Float:default
price = fields.Float:default
total_price = fields.Float:default
report_id = fields.Many2one:ondelete

### Model : inventory.change.type
is_portal_user = fields.Boolean:



