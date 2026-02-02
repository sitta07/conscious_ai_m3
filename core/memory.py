import chromadb
import time

class Memory:
    def __init__(self, db_path: str = "./data/memory_db"):
        # สร้าง Client เพื่อคุยกับ Database ในเครื่อง M3 ของเรา
        self.client = chromadb.PersistentClient(path=db_path)
        # สร้างคอลเลกชัน "ลิ้นชักความจำ"
        self.collection = self.client.get_or_create_collection(name="ai_consciousness")

    def save(self, text: str, metadata: dict = None):
        """บันทึกความจำลง Hard Drive"""
        mem_id = f"mem_{int(time.time())}"
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else [{"source": "interaction"}],
            ids=[mem_id]
        )
        print(f"💾 บันทึกความทรงจำแล้ว: {text[:30]}...")

    def recall(self, query: str, n_results: int = 2):
        """ดึงความจำที่ใกล้เคียงที่สุดออกมา"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

if __name__ == "__main__":
    my_mem = Memory()
    # ลองทดสอบบันทึก
    my_mem.save("ฉันชื่อ Sitta กำลังสร้าง AI ที่มีจิตสำนึกบน MacBook M3")
    # ลองเรียกความจำ
    context = my_mem.recall("ฉันกำลังทำโปรเจกต์อะไรอยู่?")
    print(f"🧠 ความจำที่ดึงได้: {context}")