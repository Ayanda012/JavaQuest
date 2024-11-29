from django.urls import path
from Journey import views

urlpatterns=[
    path('',views.my_login,name='login'),
    path('register',views.register_page,name='register'),
    path('main',views.main,name='main'),
    path('impact/', views.impact_view, name='impact'),
    path('donate/', views.donation_view, name='donate'),
    path('donation-success/', views.donation_success_view, name='donation_success'),
    #path('stripe-donation/<int:amount>/', views.stripe_donation_view, name='stripe_donation'),
    #path('paystack-donation/', views.paystack_donation_view, name='paystack_donation'),
    #path('paystack-callback/', views.paystack_callback_view, name='paystack_callback'),
    #path('paypal-donation/<int:amount>/', views.paypal_donation_view, name='paypal_donation'),
    path('challenges/', views.challenges_view, name='challenges'),
    path('goals/', views.goals_view, name='goals'),
    path('rewards/', views.rewards_view, name='rewards'),
    path('donate_pads/<int:pads_donated>/', views.donate_pads, name='donate_pads'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('badges/', views.badges_view, name='badges'),
     path('initiate-snapscan/<int:amount>/', views.initiate_snapscan_payment, name='initiate_snapscan'),
    path('snapscan-callback/', views.snapscan_callback, name='snapscan_callback'),
]