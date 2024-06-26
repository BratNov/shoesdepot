# Project Description

For my exam at SoftUni for the Python Web Django Framework course, I created an online store project.

## Users:

- **Customers**: Users who have access to the main functionality of the store.
- **Moderators** (store administrators): They can add, edit, and delete products, view all orders, and change their statuses. This type of user does not have access to the Django admin.
- **Administrators**: They have access to the Django admin and can change a user's status to Moderator, create product categories, sizes, and perform all other functionalities available through the Django admin.

## Pages:

- **Home**: Displays 8 randomly selected products. Also shows search results.
- **product/<str:slug>/**: Displays information about the product with an option to add it to the cart, including selecting size and quantity. The quantity of added products updates next to the cart icon. A modal window appears upon adding the product to the cart to prevent multiple clicks on the "Add to Cart" button. Adding to the cart is done via a JSON request. The cart is stored in the session. Below the product information, a section titled "You might also like" displays 8 products from the same category. If there are not enough products from the same category, products from other categories are displayed to complement the list. Additionally, if the product is on sale elsewhere in the store, the old and new prices along with the percentage discount are displayed. The breadcrumb navigation is provided.
- **category/<str:category_slug>/**: Displays products from the respective category with pagination and breadcrumb navigation. Users can choose to view all products in the main category, in which case all products in the child categories are displayed. Sorting options for products include:
  - Price low to high
  - Price high to low
  - Old to new
  - New to old (default)
  - Name
- **user**: User profile with contact and address details. If these details are filled out, they automatically appear when creating an order. If not filled out, they are filled in after order creation and saved in the profile for future orders.
- **user/register**: User registration form, modified from username to email.
- **user/login**: Login for registered users with email. If the user has products in the cart and/or had a cart from a previous login, the carts are merged or added. If a product and its size exist in both the old and new carts, the quantity is taken from the new cart.
- **user/logout**: Logout. If the customer has added products to the cart, they are saved in the database.
- **user/email_change**: User email change.
- **user/change_password**: User password change.
- **user/delete**: User deletion.
- **cart/**: List of products in the cart with options to add, change quantity, and delete. If the user had an old cart, they are redirected to this page with a modal window informing them that the cart has been added or changed.
- **cart/checkout**: Creating an order with user data and products in the cart.
- **orders/**: List of orders with filtering by status and pagination. Non-moderator users can only see and access details of their own orders.
- **orders/order/<int:pk>/**: Details of the order. If the user is a moderator, they can change the status.
- **store_admin/**: Only accessible to moderators! Lists all products with buttons for editing and deleting, including pagination. Products can be filtered by:
  - Product ID
  - Product category
  - Word search in the title and description.
- **store_admin/create/**: Only accessible to moderators! Product creation. Slug is automatically generated, and moderators can only choose from child categories, they can not add products to parent categories.
- **store_admin/edit/<int:pk>/**: Only accessible to moderators! Editing a product.
- **store_admin/delete/<int:pk>/**: Only accessible to moderators! Deleting a product.

## Online Store Project Screenshots
1. **Home Page**
![Home Page](screenshots/1_home_page.png)

2. **Parent Category (All Products)**
![Parent Category (All Products)](screenshots/2_parent_category.png)

3. **Child Category**
![Child Category](screenshots/3_child_category.png)

4. **Product Details**
![Product Details](screenshots/4_product_details.png)

5. **Adding Product to Cart**
![Adding Product to Cart](screenshots/5_add_to_cart.png)

6. **Cart Summary**
![Cart Summary](screenshots/6_cart_summary.png)

7. **Cart Checkout**
![Cart Checkout](screenshots/7_cart_checkout.png)

8. **Error on Cart Checkout**
![Error on Cart Checkout](screenshots/8_cart_checkout_error.png)

9. **Order Details (Customer)**
![Order Details (Customer)](screenshots/9_order_details_customer.png)

10. **Order List (Customer)**
![Order List (Customer)](screenshots/10_order_list_customer.png)

11. **Registration**
![Registration](screenshots/11_registration.png)

12. **Login**
![Login](screenshots/12_login.png)

13. **Merging Carts after Login**
![Merging Carts after Login](screenshots/13_merge_carts.png)

14. **Adding Cart after Login**
![Adding Cart after Login](screenshots/14_add_cart_after_login.png)

15. **User Profile**
![User Profile](screenshots/15_user_profile.png)

16. **User Password Change**
![User Password Change](screenshots/16_password_change.png)

17. **User Deletion**
![User Deletion](screenshots/17_user_deletion.png)

18. **User Email Change**
![User Email Change](screenshots/18_email_change.png)

19. **Order List (Moderator)**
![Order List (Moderator)](screenshots/19_order_list_moderator.png)

20. **Order Details (Moderator)**
![Order Details (Moderator)](screenshots/20_order_details_moderator.png)

21. **Product Creation (Moderator)**
![Product Creation (Moderator)](screenshots/21_product_creation.png)

22. **Product Deletion (Moderator)**
![Product Deletion (Moderator)](screenshots/22_product_deletion.png)

23. **Product Editing (Moderator)**
![Product Editing (Moderator)](screenshots/23_product_editing.png)

24. **Product List (Moderator)**
![Product List (Moderator)](screenshots/24_product_list_moderator.png)

