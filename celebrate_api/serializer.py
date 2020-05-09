import re
from rest_framework import serializers

def isValidePhoneNumber(s): 
      
    # 1) Begins with 0 or 91 
    # 2) Then contains 7 or 8 or 9. 
    # 3) Then contains 9 digits 
    if len(s) != 12:
        raise serializers.ValidationError("invalid phone number")
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
    if not Pattern.match(s):
        raise serializers.ValidationError("invalid phone number")     

class sendOtpSerializers(serializers.Serializer):
    userPhoneNumber = serializers.CharField(required=False,max_length=12, validators=[isValidePhoneNumber])
    userIpAddress   = serializers.CharField(required=True, max_length=32)
    userEmail       = serializers.EmailField(required=False)
    action          = serializers.CharField(required=False)

    def validate(self,data):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({"InvalidField":"Unknown field(s): {}".format(", ".join(unknown))})

        if not("userPhoneNumber" in data or "userEmail" in data):
            raise serializers.ValidationError("Phone or email field is must")
        if "action" in data and data["action"] != "forgetPassword":
            raise serializers.ValidationError("invalid value of action")
        return data

class signupSerializers(serializers.Serializer):
    userPhoneNumber = serializers.CharField(required=True,max_length=12, validators=[isValidePhoneNumber])
    userIpAddress   = serializers.CharField(required=True, max_length=32)
    otp             = serializers.CharField(required=True, max_length=10)
    userPassword    = serializers.CharField(required=True, max_length=20)

    def validate(self,data):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({"InvalidField":"Unknown field(s): {}".format(", ".join(unknown))})

class loginSerializers(serializers.Serializer):
    userPhoneNumber = serializers.CharField(required=True,max_length=12, validators=[isValidePhoneNumber])
    userIpAddress   = serializers.CharField(required=False, max_length=32)
    userPassword    = serializers.CharField(required=True, max_length=20)

    def validate(self,data):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({"InvalidField":"Unknown field(s): {}".format(", ".join(unknown))})

class apiSerializer(serializers.Serializer):
    method = serializers.CharField(required=True, max_length=32)
    action = serializers.CharField(required=True, max_length=32)
    def validate(self,data):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({"InvalidField":"Unknown field(s): {}".format(", ".join(unknown))})
        return data

class createapiSerializers(serializers.Serializer):
    url         = serializers.CharField(required=True, max_length=32)
    requestType = serializers.CharField(required=True, max_length=32)
    api         = serializers.DictField(required=True)
    validation  = serializers.CharField(required=False, max_length=32)
    auth        = serializers.CharField(required=False)
   
    def validate(self,data):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({"InvalidField":"Unknown field(s): {}".format(", ".join(unknown))})
        isValid = apiSerializer(data=data["api"])
        if not(isValid.is_valid()):
            raise serializers.ValidationError(isValid.errors)
        
        return data

    
