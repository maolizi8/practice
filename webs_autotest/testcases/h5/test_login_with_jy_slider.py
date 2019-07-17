from business.h5_login import Login
import pytest



        
@pytest.mark.test_login
def test_login(selenium):
    login=Login(selenium)
    login.login_init('USERNAME','PASSWORD')
    
        