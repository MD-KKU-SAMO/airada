# AIRADA
**AIRADA** — **A**IRADA **I**s **R**ecord **A**nd **D**ocument **A**ssembler. 


**ไอรดา** คือ โปรแกรมาสำหรับแปลงข้อมูล JSON ที่ได้รับจากเว็บ [samoHub](localhost) เป็นไฟล์ `.docx` และ `.pdf` เพื่ออำนวยความสะดวกเบื่องต้นให้กับผู้เริ่มต้นเขียนโครงการ

## แผนการดำเนินงาน
- [x] ออกแบบโครงสร้างไฟล์ JSON สำหรับเอกสารโครงการใหม่
- [ ] เขียนโปรแกรมต้นแบบ
- [ ] นำไปให้จริงกับเว็บ samoHub
- [ ] ขยายความสามารถไปสู่เอกสารต่าง ๆ

## เอกสารโครงการใหม่

TODO: เพิ่มรายละเอียดการเขียน JSON

### ตัวอย่างไฟล์ JSON สำหรับเอกสารโครงการ

```json
{
    "projectName": "ชื่อโครงการ",
    "mode": "project",
    "rationals": [ // 1. หลักการและเหตุผล,
        "Paragraph 1",
        "Paragraph 2",
    ],
    "objectives": [ // 2. วัตถุประสงค์
        "Paragraph 1",
        "Paragraph 2",
    ],
    "managers": { // 3. ผู้รับผิดชอบโครงการ
        "students": [
            {
                "name": "...",
                "id": "...",
                "role": "..."
            }
        ],
        "studentCousil": {
            "name": "...",
            "role": "..."
        },
        "contentAdvisor": "...",
        "technicalAdvisor": "..."
    },
    "nTargets": { // 4. เป้าหมายจำนวนผู้เข้าร่วมโครงการ
        "professor": 3,
        "staff": 2,
        "student": 5,
        "external": 3
    },
    "location": [ // 5. สถานที่ปฏิบัติงาน 
        "...",
        "..."
    ],
    "period": { // 6. ระยะเวลาปฏิบัติงาน
        "start": "2024-10-21",
        "end": "2025-5-25" 
    },
    "steps": [ // 7. แผนปฏิบัติงาน
        { // step 1 = array[0]
            "step": "...",
            "start": "2024-10-2",
            "end": "2024-10-5",
            "manager": "..."
        },
        {
            "step": "...",
            "start": "...",
            "end": "...",
            "manager": "..."
        },
    ],
    "programmes": { // 8. กำหนดการ
        "start": "2025-10-20",
        "end": "2025-10-21",
        "location": "...",
        "2025-10-20": [
            { //activity 1
                "activity": "...",
                "start": "...", // time
                "end": "...",
            },
            { //activity 2
                "activity": "...",
                "start": "...", // time
                "end": "...",
            },
        ],
        "2025-10-21": [
            { //activity 1
                "activity": "...",
                "start": "...", // time
                "end": "...",
            }
        ]
    },
    "budgets": [ // 9. งบประมาณการจัดกิจกรรม
        {
            "item": "item 1",
            "price": 210
        },
        {
            "item": "item 2",
            "price": 500
        }
    ],
    "ratingForm": "link to form", // 10. การประเมินโครงการ
    "consequences": [ //11. ผลที่คาดว่าจะได้รับ พร้อมค่าเป้าหมาย"
        {
            "OKR": "KR1 O1",
            "KPI": "เป้าหมายของ KR"
        },
        {
            "OKR": "KR2 O1",
            "KPI": "เป้าหมายของ KR"
        }
    ],
    "activityCredits": [ // 12. หน่วยกิจกรรมการเรียนรู้...
        { // ข้อ 1 (index 0)
                "organizer": false,
                "participant": false
        },
        { // ข้อ 2
                "organizer": true,
                "participant": false
        }
        // ... ถึงข้อ 12
    ],
    "skillCredits": { // 13. ทักษะที่คาดว่าผู้จัดและผู้เข้าร่วมโครงการจะได้รับการพัฒนา
        { // ข้อ 1
                "organizer": false,
                "participant": false
        },
        // ... ถึงข้อ 10
    },
    "mostExpectedSkill" : { // 14. ทักษะที่...จะได้รับการพัฒนามากที่สุด
        "organizer": 1, // เป็นเลขอ้างอิงจากข้อ 13, เริ่มนับจาก 0
        "participant": 2 
    } 
}
```