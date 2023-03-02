from vendor.models import Vendor
def get_vendor(request):
    try:
        vendor=Vendor.objects.get(vendor_user=request.user)
    except:
        vendor=None
    return dict(vendor=vendor)
