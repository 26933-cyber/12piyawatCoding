
print('โปรแกรมคำนวนคะแนน')

score_1 = int(input("คะแนนรวมวิชาภาษาอังกฤษ \n"))

score_2 = int(input("คะแนนรวมวิชาชีวะ_1 \n"))

score_3 = int(input("คะแนนรวมวิชาคณิต \n"))


totle_score =  score_1 + score_2 + score_3

averag = (score_1 + score_2 + score_3)/3

print("คะแนนรวม ; ",totle_score, )

print("คะแนนเฉลี่ย ; ",averag, )

if averag >=80:
    print("ระดับคะแนน ดีเยียม" )

elif averag  >=60:
    print("ระดับคะแนน ปานกลาง" )

else:
    print("ระดับคะแนน ตำ่")
 

print("wed by guy naja") 



