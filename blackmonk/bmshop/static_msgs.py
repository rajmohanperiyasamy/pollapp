from django.utils.translation import gettext_lazy as _

ADMIN_MSG={
             'SUS':_('Settings Updated Successfully.'),
             'CUS':_('Category Updated Successfully.'),
             'CDD':_('Category Deleted Successfully.'),
             'MDS':_('Manufacturer(s) Deleted Successfully.'),
             'PUD':_('Manufacturer has been updated Successfully.'),
             'DUS':_('Delivery time Updated Successfully.'),
             'DAS':_('Delivery time Added Successfully.'),
             'PUS':_('Payment Settings Updated Successfully.'),
             'DTS':_('Delivery Time Deleted Successfully.'),
             'SSU':_('Shipment Settings Updated Successfully.'),
             'OOPS':_('Oops !!! Not able to process your request.'),
}
STAFF_MSG={
            'GAS':_('Product has been updated successfully.'),
            'PUS':_('Property has been updated successfully.'),
            'PGS':_('Property Group has been updated successfully.'),
            'P':_('Selected product(s) has been published successfully'),
            'B':_('selected product(s) has been blocked'),
            'SPD':_('Selected product(s) has been deleted successfully'),
            'PSD':_('Selected property has been deleted successfully'),
            'PGD':_('Selected property group has been deleted successfully'),
            'SEO':_('SEO for the product has been updated successfully'),
            'OOPS':_('Sorry there is a problem! Your action cannot be performed, Please try later.')
}
USER_MSG={
            'OOPS':_('Sorry there is a problem! Your action cannot be performed, Please try later.'),
            'WDS':_('Your wishlist item has been deleted successfully'),
}