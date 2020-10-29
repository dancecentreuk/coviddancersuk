from django.urls import path
from .views import index, talent, talent_detail, search_talent, employers, search_employer, add_candidate_review, \
    edit_candidate_review

urlpatterns = [

    path('', index, name='index'),
    path('talent/', talent, name='talents'),
    path('talent/<pk>/<first_name>-<last_name>/', talent_detail, name='talent-detail'),
    path('search/talent/', search_talent, name='search-talent'),
    path('employer/', employers, name='employers'),
    path('search/employer/', search_employer, name='search-employer'),
    path('add-candidate-review/<int:id>/', add_candidate_review, name='add-candidate-review'),
    path('edit-candidate-review/<int:candidate_id>/<int:review_id>/', edit_candidate_review, name='edit-candidate-review')

]