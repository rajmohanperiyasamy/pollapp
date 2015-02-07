from django.utils.translation import gettext_lazy as _


EVENT_MSG={
             'WpMt':_('Event has been Submitted successfully and is under review'),
             'Wpus':_('Event has been updated successfully'),
             'ECD':_('You cannot delete this event(s), Please try later'),
             'ESUS':_('SEO for the event has been updated successfully.'),
             'ELUS':_('Event Listing type has been updated successfully.'),
             'EDS':_('The Selected event(s) has been deleted successfully'),
             'P':_('The selected event(s) has been published successfully'),
             'R':_('The selected event(s) has been rejected'),
             'B':_('The selected event(s) has been blocked'),
             'err':_('Sorry there is a problem! Your action cannot be performed, Please try later.'),
             'SAV':_('The Venue has been added successfully'),
             'OOPS':_('Oops !!! Not able to process your request.'),
}
ARTICLE_MSG={
             'YAS':_('Article has been added successfully'),
             'YUS':_('Article has been updated successfully'),
             'ADS':_('Venue Sussessfully Deleted'),
             'AND':_('Sorry you don\'t have permission to delete this venue' ),
             'ASUS':_('SEO for the article has been updated successfully'),
             'P':_('The Selected article(s) has been published successfully'),
             'R':_('The selected article(s) has been rejected'),
             'B':_('The selected article(s) has been blocked'),
             'SAD':_('The Selected article(s) has been deleted successfully'),
             'err':_('Sorry there is a problem! Your action cannot be performed, Please try later'),
             'AAS':_('The Venue has been added successfully'),
             'OOPS':_('Oops !!! Not able to process your request.'),
}
CLASSIFIED_MSG={
                'CAS':_('Classified Ad listing has been added successfully.'),
                'CUS':_('Classified Ad listing has been updated successfully.'),
                'CSUS':_('SEO for the Classified Ad listing has been updated successfully.'),
                'CDS':_('Classified Ad Listing(s) has been deleted successfully.'),
                'CSCS':_('Classified Ad listing(s) status has been changed successfully.'),
                'CLUS':_('Classified Listing Type has been updated successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.')
}
GALLERY_MSG={
                'AAS':_('Album has been added successfully.'),
                'AUS':_('Album has been updated successfully.'),
                'ASS':_('Album has been saved successfully.'),
                'ASUS':_('SEO for the album has been updated successfully.'),
                'ADS':_('Album has been deleted successfully.'),
                'APUS':_('Album-Photo details has been updated successfully.'),
                'APDS':_('Album-photo has been deleted successfully.'),
                'AFSCS':_('Album(s) has been featured successfully.'),
                'AFSNCS':_('Album(s) has been Non-featured successfully.'),
                'ASCS':_('Album(s) status has been changed successfully.'),
                'ALUS':_('Album Listing type has been changed successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.')
}
BOOKMARK_MSG={
                 'BAS':_('Bookmark has been added successfully'),
                 'BUS':_('Bookmark has been updated successfully'),
                 'BSUS':_('SEO for the Bookmark has been updated successfully'),
                 'P':_('The Selected Bookmark(s) has been published successfully'),
                 'R':_('The selected Bookmark(s) has been rejected'),
                 'B':_('The selected Bookmark(s) has been blocked'),
                 'SBD':_('The Selected Bookmark(s) has been deleted successfully'),
                 'err':_('Sorry there is a problem! Your action cannot be performed, Please try later'),
                 'OOPS':_('Oops !!! Not able to process your request.'),
}
ATTRACTION_MSG={
                'AAS':_('Attraction details has been added successfully.'),
                'AUS':_(' Attraction details has been updated successfully.'),
                'ASUS':_('SEO for the attraction has been updated successfully.'),
                'AFSCS':_('Attraction has been added as featured/basic successfully.'),
                'ADS':_('Selected Attraction(s) has been deleted successfully.'),
                'ASCS':_('Attraction(s) status has been changed successfully.'),
                'ALUS':_('Attraction listing type has been updated successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.')
}
LOCALITY_MSG={
              'SAV':_('Venue details has been added successfully.'),
              'OOPS':_('Sorry! Your request cannot be processed, Please try again later.')
}
BUSINESS_MSG={
                'BAS':_('Business listing has been added successfully.'),
                'BUS':_('Business listing has been updated successfully.'),
                'BASTO':_('Your business listing has been submitted and under review.'),
                'BSUS':_('SEO for the business listing has been updated successfully.'),
                'BDS':_('Business listing(s) has been deleted successfully.'),
                'BSCS':_('Business listing(s) status has been changed successfully.'),
                'BLUS':_('Business listing Type has been updated successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.'),
                'BPUS':_('Business listing-Product has been updated successfully.'),
                'BPDS':_('Business listing-Product has been deleted successfully.'),
                'BCUS':_('Business listing-Coupon has been updated successfully.'),
                'BCDS':_('Business listing-Coupon has been deleted successfully.'),
                'BAUS':_('Business listing-Address has been updated successfully.'),
                'BADS':_('Business listing-Address has been deleted successfully.')
}
USERMGMT_MSG={
              'PSU':_('Your profile has been updated successfully.'),
              'OOPS':_('Sorry there is a problem! Your action cannot be performed, Please try later.'),
              'EAU':_('Sorry! E-mail is already used.'),
              'UPS':_('Your password has been updated successfully'),
              'CSU':_('Your contact info has been updated successfully.'),
              'PPU':_('Your preferences has been updated successfully.')
}

CONTACT_MSG = {
            'ADAS':_("Thanks for you enquiry, Our executive will get back to you shortly."),
            'CNAS':_("Thanks for contacting us, we'll get back to you shortly."),
            'ADWS':_("Thanks for Advertising with us, we'll get back to you shortly."),
}