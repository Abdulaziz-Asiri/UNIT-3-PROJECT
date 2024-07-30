from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .models import Product,Supplier , Category



def all_products_view(request:HttpRequest ):
    products = Product.objects.all()
    return render(request, "allProducts.html", {"products":products})

def delete_products_view(request:HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect("product:all_products_view")

def add_products_view(request: HttpRequest):
    products = Product.objects.all()
    category = Category.objects.all()
    allSuppliers = Supplier.objects.all() 
    if request.method == "POST":
        category_id = request.POST['category']
        category_instance = Category.objects.get(id=category_id)
        new_product = Product(name=request.POST['name'],
                                description=request.POST['description'],
                                price=request.POST['price'],
                                category= category_instance,
                                image= request.FILES['image'])
        new_product.save()
        supplier_ids = request.POST.getlist('suppliers')
        suppliers = Supplier.objects.filter(id__in=supplier_ids)
        new_product.suppliers.add(*suppliers)

    return render(request, "addProducts.html",  {"products": products,"categories":category,"suppliers": allSuppliers})

def update_products_view(request:HttpRequest, product_id:int):
    products = Product.objects.get(id=product_id)
    if request.method == "POST":
        products.name = request.POST["name"]
        products.description = request.POST["description"]
        products.price = request.POST["price"]
        products.image = request.POST["image"]
        products.category = request.POST["category"]
        products.suppliers = request.POST["suppliers"]
        products.save()
        return redirect('product:all_products_view')
    
    return render(request, "product:add_products_view", {"products":products})



