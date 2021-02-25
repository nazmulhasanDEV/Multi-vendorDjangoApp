const service_type = document.getElementById('service_type');
const service_category_by_type = document.getElementById('service_category_by_type');
const service_subcategory = document.getElementById('service_subcategory');

let createServiceCategoryOption, grabed_service_categories;
let createSubCategoryOption, grabed_service_subcategories;


// starts addEventListener function
service_type.addEventListener('change', function(){

service_category_by_type.innerHTML = "<option>---Choose Service Category---</option>";

// ajax request starts
$.ajax({
url:'',
type: 'get',
data: {
selected_service_type: this.value
},
success: function(response){
grabed_service_categories = response.service_cats_by_service_type;
console.log(grabed_service_categories);
// map function starts
grabed_service_categories.map(items=>{
createServiceCategoryOption             = document.createElement('option');

if (items.name){
createServiceCategoryOption.textContent = items.name;
}else{
createServiceCategoryOption.textContent = items.service_name;
}

createServiceCategoryOption.value       = items.id;
service_category_by_type.appendChild(createServiceCategoryOption);

});
// map function ends
}

});
// ajax request ended

});
// ends addEventListener function

// starts addEventListener function
service_category_by_type.addEventListener('change', function(){

service_subcategory.innerHTML = "<option>---Choose Sub-category---</option>";

// ajax request starts
$.ajax({
url:'',
type: 'get',
data: {
selected_category_by_service: this.value,
selected_serviceType: service_type.value
},
success: function(response){

grabed_service_subcategories = response.service_subcats_by_cat;
console.log(grabed_service_subcategories);

// starts map function
grabed_service_subcategories.map(items=>{

createSubCategoryOption             = document.createElement('option');
if (items.name){
createSubCategoryOption.textContent = items.name;
createSubCategoryOption.value       = items.id;
}else{
createSubCategoryOption.textContent = items.subcategory_name;
createSubCategoryOption.value       = items.id;
}
service_subcategory.appendChild(createSubCategoryOption);

});
// ends map function

}

});
// ajax request ended



});
// ends addEventListener function





