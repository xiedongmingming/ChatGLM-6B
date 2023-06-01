import chromadb

from chromadb.config import Settings

# client = chromadb.Client()

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=".chromadb/"  # Optional, defaults to .chromadb/ in the current directory
))

client.persist()

# client.heartbeat() # returns a nanosecond heartbeat. Useful for making sure the client remains connected.
# client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.

collection = client.create_collection(name="collection")  # 集合是存储嵌入、文档和任何其他元数据的地方

collection.add(  # 添加一些文本文档到集合中，CHROMA将存储文本，并自动处理标记化、嵌入和索引
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
)

# collection.add( # 如果已经自己生成了嵌入向量，则可以直接加载
#     embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
#     documents=["This is a document", "This is another document"],
#     metadatas=[{"source": "my_source"}, {"source": "my_source"}],
#     ids=["id1", "id2"]
# )

# 查询CHROMA中的数据--CHROMA会返回N个最相似的结果
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2
)

# 默认情况下，CHROMA使用内存数据库，该数据库在退出时持久化并在启动时加载（如果存在）。

# chroma_client.persist()
