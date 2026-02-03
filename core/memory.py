import chromadb
import time
from typing import List, Optional, Dict, Any

class Memory:
    def __init__(self, db_path: str = "./data/memory_db"):
        # สร้าง Client เชื่อมต่อกับ Database ในเครื่อง
        self.client = chromadb.PersistentClient(path=db_path)
        
        # สร้างลิ้นชักเก็บความจำชื่อ "ai_consciousness"
        self.collection = self.client.get_or_create_collection(name="ai_consciousness")

    def save(self, text: str, metadata: dict = None):
        """บันทึกความจำลง Hard Drive"""
        # สร้าง ID ไม่ซ้ำกันด้วยเวลาปัจจุบัน
        mem_id = f"mem_{int(time.time() * 1000)}"
        
        if metadata is None:
            metadata = {"source": "interaction", "timestamp": time.time()}
        else:
            metadata["timestamp"] = time.time()
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[mem_id]
        )
        print(f"💾 Saved: {text[:50]}...")

    def recall(self, query: str, n_results: int = 5) -> List[str]: 
        """นึกถึงความจำที่เกี่ยวข้องกับเรื่องนี้"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            # ดึงข้อมูลออกมาทั้งหมดที่เจอ
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            print(f"Memory Recall Error: {e}")
            return []

    def recall_with_metadata(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Recall memories with full metadata including timestamp."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            memories = []
            if results['documents']:
                for doc, metadata, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    memories.append({
                        "text": doc,
                        "metadata": metadata,
                        "similarity": 1 - distance,  # Convert distance to similarity
                        "timestamp": metadata.get("timestamp", 0)
                    })
            return memories
        except Exception as e:
            print(f"Memory Recall Error: {e}")
            return []

    def find_similar_facts(self, fact: str, n_results: int = 3) -> List[str]:
        """Find semantically similar facts to detect duplicates."""
        return self.recall(fact, n_results)

    def get_all_memories(self) -> List[str]:
        """Get all stored memories (for introspection)."""
        try:
            # Get all items in collection
            all_results = self.collection.get(include=['documents'])
            return all_results['documents'] if all_results['documents'] else []
        except Exception as e:
            print(f"Failed to get all memories: {e}")
            return []
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