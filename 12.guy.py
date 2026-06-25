print("โปรแกรมคำนวนค่าไฟ โดย ปิยวัฒน์ คำนวน กาย")

Electricity_bill = int(input("กรุณากรอกค่าไฟของท่าน \n "))

if Electricity_bill <= 9:
   
   print("ค่าไฟฟรี")

elif Electricity_bill <= 50: 
   
     print("ค่าไฟ 2บาท/หน่วย")

elif Electricity_bill <= 100: 

     print("ค่าไฟ 3บาท/ต่อหน่วย")

else:
    print("ค่าไฟ 4บาท/ต่อหน่วย")