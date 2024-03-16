from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

def test_patch_order_by_id():
    # created new order
    test_endpoint = "/store/order"
    data = {
        'pet_id': 0
    }
    response = api_helpers.post_api_data(test_endpoint, data)
    order_data = response.json()
    assert response.status_code == 201
    validate(instance=order_data, schema=schemas.order)

    # make sure the pet with pet_id is changed to pending after the order is placed
    test_endpoint = "/pets/0"
    response = api_helpers.get_api_data(test_endpoint)
    updated_pet_data = response.json()
    assert updated_pet_data.get('status') == 'pending'
    
    # updated the newly created order to pending using patch
    patch_endpoint ="/store/order/{}".format(order_data.get('id'))
    new_data = {
        'status': 'available'
    }
    patch_response = api_helpers.patch_api_data(patch_endpoint, new_data)
    
    assert patch_response.status_code == 200
    assert patch_response.json()["message"] == "Order and pet status updated successfully"

    # after patching the status of pet with pet_id should be updated to available
    test_endpoint = "/pets/0"
    response = api_helpers.get_api_data(test_endpoint)
    updated_pet_data = response.json()
    
    assert updated_pet_data.get('status') == 'available'
    
    
    