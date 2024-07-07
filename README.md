# siou/airada

![](/doc/mascot-ai-1.png)

**airada** — **a**irada **i**s **r**ecord **a**nd **d**ocument **a**ssembler. 

**airada (ไอรดา)** คือ โปรแกรมาสำหรับแปลงข้อมูล JSON ที่ได้รับจากเว็บ [samoHub](localhost) เป็นไฟล์ `.docx` เพื่ออำนวยความสะดวกเบื่องต้นให้กับผู้เริ่มต้นเขียนโครงการและเอกสารอื่น ๆ ของสโม ฯ ในอนาคต

airada เป็นส่วนหนึ่งของโครงการ siou (samoIT Open Utilities) — ผู้ที่สนใจสามารถ contribute โค้ดให้กับ airada ได้โดยการเปิด pull request

## แผนการดำเนินงาน

- [x] ออกแบบโครงสร้างไฟล์ JSON สำหรับเอกสารโครงการใหม่
- [ ] เขียนโปรแกรมต้นแบบ
    - [x] จัดการข้อความปกติได้
    - [x] จัดการตารางข้อความได้
    - [ ] จัดการตารางติ๊กถูกได้
    - [ ] ใส่ QR code ได้
- [ ] นำไปให้จริงกับเว็บ samoHub
- [ ] ขยายความสามารถไปสู่เอกสารต่าง ๆ

## เอกสารโครงการใหม่

TODO: เพิ่มรายละเอียดการเขียน JSON

### ตัวอย่างไฟล์ JSON สำหรับเอกสารโครงการ
กรุณาดูตัวอย่างใน `test/project-paper.json`

## Attribution
### Projects
- [python-docx](https://pypi.org/project/python-docx/) — for `.docx` functionality.
- [python-docx-replace](https://pypi.org/project/python-docx-replace/) — for implementation of replace functionality
- [money](https://pypi.org/project/money/) — for safe money management lib.
- [num-thai](https://pypi.org/project/num-thai/) — for number to Thai text function.

### People
- **มทินา อัศวเมธาพันธ์** — beta tester and bug-hunter

### Tools
- [akuma.ai](https://akuma.ai/) — inital art for airada mascot. Will hire actual artist if budget permits.

## License

MIT License

## Author
- **กฤษฎิ์ ปัจญรัตน์** — inital developer
 
ในนามของสโมสรนักศึกษา คณะแพทยศาสตร์ มหาวิทยาลัยขอนแก่น ปี 2567