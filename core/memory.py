import chromadb
import time

class Memory:
    def __init__(self, db_path: str = "./data/memory_db"):
        # สร้าง Client เชื่อมต่อกับ Database ในเครื่อง
        self.client = chromadb.PersistentClient(path=db_path)
        
        # สร้างลิ้นชักเก็บความจำชื่อ "ai_consciousness"
        self.collection = self.client.get_or_create_collection(name="ai_consciousness")

    def save(self, text: str, metadata: dict = None):
        """บันทึกความจำลง Hard Drive"""
        # สร้าง ID ไม่ซ้ำกันด้วยเวลาปัจจุบัน
        mem_id = f"mem_{int(time.time())}"
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else [{"source": "interaction"}],
            ids=[mem_id]
        )
        print(f"💾 Saved: {text}")

    def recall(self, query: str, n_results: int = 1):
        """นึกถึงความจำที่เกี่ยวข้องกับเรื่องนี้"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        # ถ้าเจอความจำ ให้ส่งกลับมาเป็นข้อความ
        return results['documents'][0] if results['documents'] else []

# ส่วนทดสอบ (รันตรงนี้เพื่อเช็คว่าทำงานได้ไหม)
if __name__ == "__main__":
    my_mem = Memory()
    
    # 1. ลองบันทึก
    print("...กำลังทดสอบบันทึกความจำ...")
    my_mem.save("ฉันชื่อ Sitta ผู้สร้างโปรเจกต์นี้")
    my_mem.save("โปรเจกต์นี้รันบน MacBook M3")
    
    # 2. ลองนึก (Recall)
    print("...กำลังทดสอบการนึก...")
    mem = my_mem.recall("ใครเป็นคนสร้างโปรเจกต์นี้?")
    print(f"🧠 AI นึกออกว่า: {mem}")