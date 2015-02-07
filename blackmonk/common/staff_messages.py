from django.utils.translation import gettext_lazy as _

COMMON={
        'DENIED':_("Permission Denied.You don't have access to proccess this request"),
}

EVENT_MSG={
             'YES':_('Event has been added successfully'),
             'EUP':_('Event has been updated successfully'),
             'ECD':_('You cannot delete this event(s), Please try later'),
             'ESUS':_('SEO for the event has been updated successfully.'),
             'ELUS':_('Event Listing type has been updated successfully.'),
             'EDS':_('The Selected event(s) has been deleted successfully'),
             'P':_('The selected event(s) has been published successfully'),
             'R':_('The selected event(s) has been rejected'),
             'B':_('The selected event(s) has been blocked'),
             'err':_('Sorry there is a problem! Your action cannot be performed, Please try later.'),
             'SAV':_('The Venue has been added successfully'),
             'SUV':_('The Venue has been updated successfully'),
             'OOPS':_('Oops !!! Not able to process your request.'),
             'EMPT':_('Not able to process your request. Empty CSV file!'),
}
ADVICE_MSG={
            'AAS':_('Question has been added successfully.'),
            'AUS':_('Question has been updated successfully.'),
            'ASUS':_('SEO for the Thread has been updated successfully.'),
            'QDS':_('Question(s) has been deleted successfully.'),
            'PDS':_('Post(s) has been deleted successfully.'),
            'ADS':_('Answer(s) has been deleted successfully.'),
            'ASCS':_('Thread(s) status has been changed successfully.'),
            'AAUS':_('Thread-Answer status has been changed successfully.'),
            'AADS':_('Delete successfully.'),
            'OOPS':_('Sorry! Your request cannot be processed, Please try again later.'),
            'DENIED':_("Permission Denied.You don't have access to proccess this request"),
            'CDS':_('Comment has been deleted successfully.'),
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
             'EMPT':_('Not able to process your request.Empty CSV file!'),
             'CAS': _("Success"),
}
BOOKMARK_MSG={
             'YBS':_('Bookmark has been added successfully'),
             'YBUS':_('Bookmark has been updated successfully'),
             'BSUS':_('SEO for the Bookmark has been updated successfully'),
             'P':_('The Selected Bookmark(s) has been published successfully'),
             'R':_('The selected Bookmark(s) has been rejected'),
             'B':_('The selected Bookmark(s) has been blocked'),
             'BDS':_('The Selected Bookmark(s) has been deleted successfully'),
             'err':_('Sorry there is a problem! Your action cannot be performed, Please try later'),
             'OOPS':_('Oops !!! Not able to process your request.'),
}
DEAL_MSG={  
             'YDS':_('Deal has been added successfully'),
             'YUS':_('Deal has been updated successfully'),
             'ASUS':_('SEO for the deal has been updated successfully'),
             'P':_('The Selected deal(s) has been activated successfully'),
             'B':_('The Selected deal(s) has been deactived successfully'),
             'err':_('Sorry your  action can\'t completed,please try again'),
             'SDD':_('Selected deal(s) deleted successfully.'),
             'AAS':_('Address Successfully Added.'),
             'OOPS':_('Oops !!! Not able to process your request.'),
}
CLASSIFIED_MSG={
                'CAS':_('Classified Ad listing has been added successfully.'),
                'CUS':_('Classified Ad listing has been updated successfully.'),
                'CSUS':_('SEO for the Classified Ad listing has been updated successfully.'),
                'CDS':_('Classified Ad Listing(s) has been deleted successfully.'),
                'CSCS':_('Classified Ad listing(s) status has been changed successfully.'),
                'CLUS':_('Classified Listing Type has been updated successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.'),
                'EMPT':_('Your request cannot be processed. Empty CSV file!')
}
GALLERY_MSG={
                'AAS':_('Album has been added successfully.'),
                'AUS':_('Album has been updated successfully.'),
                'ASS':_('Album has been saved successfully.'),
                'ASUS':_('SEO for the album has been updated successfully.'),
                'ADS':_('Album(s) has been deleted successfully.'),
                'APUS':_('Album-Photo details has been updated successfully.'),
                'APDS':_('Album-photo has been deleted successfully.'),
                'AFSCS':_('Album(s) has been featured successfully.'),
                'AFSNCS':_('Album(s) has been Non-featured successfully.'),
                'ASCS':_('Album(s) status has been changed successfully.'),
                'ALUS':_('Album Listing type has been changed successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.')
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
              'SUV':_('Venue details has been updated successfully.'),
              'OOPS':_('Sorry! Your request cannot be processed, Please try again later.')
}

ENQUIRY_MSG={
              'EMR':_('Enquiry marked as Read.'),
              'EMUR':_('Enquiry marked as Unread'),
              'EDS':_('Enquiry deleted successfully')
}

BUSINESS_MSG={
                'BAS':_('Business listing has been added successfully.'),
                'BUS':_('Business listing has been updated successfully.'),
                'BSUS':_('SEO for the business listing has been updated successfully.'),
                'BDS':_('Business listing(s) has been deleted successfully.'),
                'BSCS':_('Business listing(s) status has been changed successfully.'),
                'BLUS':_('Business listing Type has been updated successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.'),
                'BPUS':_('Business listing-Product has been updated successfully.'),
                'BPAS':_('Business listing-Product has been added successfully.'),
                'BPDS':_('Business listing-Product has been deleted successfully.'),
                'BCAS':_('Business listing-Coupon has been added successfully.'),
                'BCUS':_('Business listing-Coupon has been updated successfully.'),
                'BCDS':_('Business listing-Coupon has been deleted successfully.'),
                'BAUS':_('Business listing-Address has been updated successfully.'),
                'BADS':_('Business listing-Address has been deleted successfully.'),
                'EMPT':_('Your request cannot be processed. Empty CSV file!'),
}
COMMENT_MSG={
                'CDS':_('Comment(s) has been deleted successfully.'),
                'CSCS':_('Comment(s) status has been changed successfully.'),
                'CFCS':_('Comment(s) flag has been cleared successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.'),
}
VIDEO_MSG = {
              'YES':_('The selected video(s) has been added successfully'),  
              'VPS':_('The selected video(s) has been published successfully'), 
              'VPES':_('The selected video(s) has been moved to pending status.'), 
              'FBS':_(' The selected video(s) has been blocked.'), 
              'FVS':_('The selected video(s) has been featured successfully.'), 
              'UFVS':_('The selected video(s) has been Unfeatured successfully.'), 
              'VAS':_(' Video(s) has been added successfully'),
              'VUS':_('Video has been modified successfully.'),
              'VRS':_('Video has been rejected successfully.'),
              'VSUS':_('SEO for the video has been updated successfully.'),
              'EVUS':_('Video has been modified successfully.'),
              'VDS':_('The selected video(s) has been deleted successfully.'),
              'OOPS':_('Sorry there is a problem! Your action cannot be performed, Please try later.')
             
             
             }
MOVIE_MSG = {
              'YES':_(' Movie listing has been added successfully.'),   
              'MAS':_(' Movie listing has been added successfully.'),
              'MUS':_(' Movie listing has been updated successfully.'),
              'MSUS':_('SEO for the movie listing has been updated successfully.'),
              'MVUS':_('Movie listing has been updated successfully.'),
              'MDS':_(' Movie listing has been deleted successfully.'),
              'MSCS':_('Movie(s) Status Changed Successfully.'),
              'OOPS':_('Sorry there is a problem! Your action cannot be performed, Please try later.'),
              'MSTUS':_('Movie showtimes has been updated successfully.'),
              'MSAA':_('Movie showtimes already added.'),
              'MSDS':_(' Movie showtimes has been deleted successfully.'),
              'MSAS':_('Movie showtimes has been added successfully.'),
              'TSU':_(' SEO for the theatre listing has been updated successfully.'),
              'TU':_('Theatre listing has been updated successfully.'),
              'MES':_('Movie listing has been updated successfully.'),
              'MCRAS':_(' Movie critic review has been added successfully.'),
              'MCRDS':_('Movie critic review has been deleted successfully.'),
              'MTAS':_('Theatre listing has been added Successfully'),
              'MTUS':_('Theatre listing has been updated Successfully'),
              'TSUS':_('Theatre showtimes has been updated successfully.'),
              'TDS':_(' Theatre listing has been deleted successfully.'),
              'TSCS':_('Theatre(s) Status Changed Successfully.'),

             }
PAYMENT_MSG={
            'SUS':_('Payment done successfully.'),
            'CAN':_('Payment cancelled successfully.'),
            'FAI':_('Payment failed.'),
            'WAI':_('Payment under processing.'),
            'REV':_('Payment under review.'),
            'OOPS':_('Sorry there is a problem! Your action cannot be performed, Please try later.')
}

POLLS_MSG={
             'PAS':_('Poll has been added Successfully.'),
             'PUS':_('Poll has been updated Successfully.'),
             'CUS':_('Poll Category Updated Successfully.'),
             'PDS':_('Poll  Deleted Successfully.'),
             'CNF':_('Oops !!! Poll Category not found.'),
             'OOPS':_('Oops !!! Not able to process your request.'),
             'HSUS':_('Poll Home Page SEO Updated Successfully.'),
             'CSUS':_('Poll Category SEO Updated Successfully.'),
             'SUS':_('Poll Settings Updated Successfully.'),
             'APS':_('Poll Pricing Information Updated Successfully.'),
} 
SWEEPSTAKES_MSG={
                'SAS':_('Sweepstakes details has been added successfully.'),
                'SUS':_('Sweepstakes details has been updated successfully.'),
                'SSUS':_('SEO for the Sweepstakes has been updated successfully.'),
                'SDS':_('Selected Sweepstakes(s) has been deleted successfully.'),
                'SSCS':_('Sweepstakes(s) status has been changed successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.'),
                'SOUS':_('Sweepstakes offer has been updated successfully.'),
                'SODS':_('Sweepstakes offer has been deleted successfully.')
}

BANNER_MSG = {
                'BADAS':_('Banner details has been added successfully.'),
                'BADASOF':_('Thanks for uploading your banner, Our representative will get in touch with you shortly.'),
                'BADUS':_('Banner details has been updated successfully.'),
                'BADSUS':_('Banner Ad(s) status has been changed successfully.'),
                'OOPS':_('Sorry! Your request cannot be processed, Please try again later.'),
                'BADDS':_('Banner Ads has been deleted successfully.')
}

RESTAURANT_MSG={
             'YAS':_('Restaurant has been added successfully'),
             'RUS':_('Restaurant has been updated successfully'),
             'AND':_('Sorry you don\'t have permission to delete this venue' ),
             'ASUS':_('SEO for the restaurant has been updated successfully'),
             'P':_('The Selected restautrant(s) has been published successfully'),
             'R':_('The selected restautrant(s) has been rejected'),
             'B':_('The selected restautrant(s) has been blocked'),
             'SAD':_('The Selected restautrant(s) has been deleted successfully'),
             'err':_('Sorry there is a problem! Your action cannot be performed, Please try later'),
             'AAS':_('The Venue has been added successfully'),
             'OOPS':_('Oops !!! Not able to process your request.'),
             'RMUS':_('Restaurant listing-menu has been updated successfully.'),
             'RMDS':_('Restaurant listing-Menu has been deleted successfully.'),
             'RIUS':_('Restaurant listing-image has been updated successfully.'),
             'RIDS':_('Restaurant listing-image has been deleted successfully.'), 
             'RVUS':_('Restaurant listing-video has been updated successfully.'),
             'RVDS':_('Restaurant listing-video has been deleted successfully.'), 
             'RAS':_('Restaurant listing has been added successfully.'),
             'RUS':_('Restaurant listing has been updated successfully.'),
             'RSUS':_('SEO for the restaurant listing has been updated successfully.'),
             'RDS':_('Restaurant listing(s) has been deleted successfully.'),
             'RSCS':_('Restaurant listing(s) status has been changed successfully.'),
             'RLUS':_('Restaurant listing Type has been updated successfully.'),
}

CHANNEL_MSGS = {
            'CUS':_("Channel has been updated successfully."),
            'ERR':_('Sorry there is a problem! Your action cannot be performed, Please try later.'),
}