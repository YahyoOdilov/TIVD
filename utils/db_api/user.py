from .models import Model, BigInt, VarChar, BigAuto

class User(Model):
    id = BigAuto(null= False, primary= True)
    tid = BigInt(null= False, unique= True)
    username = VarChar(max_length=100)
    
