-- เปิดใช้งาน Extension สำหรับ Vector Search (pgvector)
-- ถ้ายังไม่ได้ติดตั้ง pgvector บนเครื่องคุณ คุณต้องติดตั้งก่อน
CREATE EXTENSION
IF NOT EXISTS vector;

-- สร้างตาราง 'documents' เพื่อเก็บข้อความและ Embedding
-- มิติของเวกเตอร์ (dimensions) ควรตรงกับโมเดล Embedding ที่คุณใช้
-- เช่น 1536 สำหรับ 'nomic-embed-text' หรือ 4096 สำหรับ 'llama3' (8B)
CREATE TABLE
IF NOT EXISTS documents
(
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR
(1024) -- เปลี่ยนตัวเลขนี้ให้ตรงกับมิติของโมเดล Embedding ของคุณ
);

-- สามารถเพิ่มคำสั่ง SQL อื่นๆ เช่น การสร้างผู้ใช้, สิทธิ์, หรือข้อมูลเริ่มต้นเพิ่มเติมได้ที่นี่
-- ตัวอย่างการเพิ่มข้อมูล dummy (ค่า embedding ต้องเป็นตัวเลขจริงจากโมเดลของคุณ)
-- INSERT INTO documents (content, embedding) VALUES
-- ('นี่คือข้อความตัวอย่างแรก', '{0.01,0.02,0.03,...,0.04}'),
-- ('นี่คือข้อความตัวอย่างที่สอง', '{0.05,0.06,0.07,...,0.08}');