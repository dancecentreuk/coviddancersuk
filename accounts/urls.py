from django.urls import path
from .views.candidate import candidate_signup, candidate_profile, candidate_bio_update,\
    candidate_experience_update, candidate_delete_photos, add_photo, add_photo_2, \
    candidate_location_update, candidate_birthday_update, update_candidate_profile_picture, CandidateVerificationView
from .views.individual import register, sign_in, logout_user, profile, RequestPassword, CompletePasswordReset
from .views.employer import employer_signup, employer_profile, update_company_profile, \
    update_company_bio, update_profile_picture



urlpatterns = [
    path('register/candidate/', candidate_signup, name='candidate-signup'),
    path('register/employer/', employer_signup, name='employer-signup'),
    path('register/', register, name='signup'),
    path('login/', sign_in, name='sign-in'),
    path('log-out/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('candidate/profile/', candidate_profile, name='candidate-profile'),
    path('employer/profile/', employer_profile, name='employer-profile'),
    path('activate/<uidb64>/<token>/', CandidateVerificationView.as_view(), name='candidate-activate'),
    path('request-reset-link', RequestPassword.as_view(), name='password-reset-link'),
    path('set-new-password/<uidb64>/<token>/', CompletePasswordReset.as_view(), name='reset-password'),


    path('candidate/bio/<pk>', candidate_bio_update, name='candidate-bio'),
    path('candidate/experience/<pk>', candidate_experience_update, name='candidate-experience'),
    path('delete/photo/<int:pk>', candidate_delete_photos, name='delete-photos'),
    path('add-photo', add_photo, name='add-photos'),
    path('add-photo_2', add_photo_2, name='manual'),
    path('update-location/<int:pk>/', candidate_location_update, name='update-location'),
    path('update-birthday/<int:pk>/', candidate_birthday_update, name='update-birthday'),
    path('update-profile_image/<int:pk>/', update_candidate_profile_picture, name='update-candidate-profile-picture'),


    path('employer/update-company-profile/<pk>/', update_company_profile, name='update-company-profile'),
    path('employer/update-company-info/<int:pk>', update_company_bio, name='update-company-info' ),
    path('employer/update-profile_image/<int:pk>', update_profile_picture, name='update-company-photo' ),
]