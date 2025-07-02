from django.shortcuts import render,redirect
from django.views.generic import View
# Create your views here.
from shop.forms import TransactionForm,CustomerForm,PhoneForm
from shop.models import Customer,Phone,Transaction,Invoice,InvoiceItem


class AddCustomerView(View):
    template_name="AddCustomer.html"
    form_class=CustomerForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']

            discount = form.cleaned_data['discount']

            Customer.objects.create(name=name, discount=discount)

            return redirect('add_customer') 

        return render(request, self.template_name, {'form': form})
    

class AddItemView(View):
    template_name="AddItem.html"
    form_class=PhoneForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            item = form.cleaned_data['item']

            price = form.cleaned_data['price']

            Phone.objects.create(item=item, price=price)

            return redirect('add_item') 

        return render(request, self.template_name, {'form': form})
    
  
class PurchasePhoneView(View):
    template_name = "PurchasePhone.html"
    form_class = TransactionForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        cart = request.session.get('cart', [])
        subtotal = sum(item['amount'] for item in cart)
        discount_percent = 0
        discount_amount = 0
        grand_total = 0

        if 'customer_id' in request.session:
            try:
                customer = Customer.objects.get(id=request.session['customer_id'])
                discount_percent = customer.discount
                discount_amount = subtotal * (discount_percent / 100)
                grand_total = subtotal - discount_amount
            except Customer.DoesNotExist:

                request.session['customer_id'] = None
                discount_percent = 0
                discount_amount = 0
                grand_total = subtotal

        return render(request, self.template_name, {
            'form': form,
            'cart': cart,
            'subtotal': subtotal,
            'discount_percent': discount_percent,
            'discount_amount': discount_amount,
            'grand_total': grand_total
        })
    
    def post(self, request, *args, **kwargs):

        if 'save_invoice' in request.POST:

            cart = request.session.get('cart', [])

            customer_id = request.session.get('customer_id')

            if not cart or not customer_id:
                return redirect('transaction_list')

            try:
                customer = Customer.objects.get(id=customer_id)

            except Customer.DoesNotExist:

                return redirect('transaction_list')

            subtotal = sum(item['amount'] for item in cart)
            discount = customer.discount
            grand_total = subtotal - (subtotal * discount / 100)

            invoice = Invoice.objects.create(
                customer=customer,
                total=subtotal,
                discount=discount,
                grand_total=grand_total
            )

            for item in cart:
                phone = Phone.objects.get(id=item['phone_id'])
                InvoiceItem.objects.create(
                    invoice=invoice,
                    phone=phone,
                    qty=item['qty'],
                    rate=item['rate'],
                    amount=item['amount']
                )


            request.session['cart'] = []
            request.session['customer_id'] = None

            return redirect('transaction_list')  

        else:

            form = self.form_class(request.POST)
            
            if form.is_valid():
                customer = form.cleaned_data['customer']
                phone = form.cleaned_data['phone']
                qty = form.cleaned_data['qty']
                rate = phone.price
                amount = qty * rate

                cart = request.session.get('cart', [])
                cart.append({
                    'phone_id': phone.id,
                    'item': phone.item,
                    'qty': qty,
                    'rate': rate,
                    'amount': amount
                })

                request.session['cart'] = cart
                request.session['customer_id'] = customer.id

                return redirect('transaction_list')

            return render(request, self.template_name, {'form': form})
        


class InvoiceListView(View):
    template_name = 'invoice_list.html'

    def get(self, request, *args, **kwargs):

        invoices = Invoice.objects.all().order_by('-created_at')

        for invoice in invoices:
            invoice.discount_amount = invoice.total * (invoice.discount / 100)

        return render(request, self.template_name, {'invoices': invoices})