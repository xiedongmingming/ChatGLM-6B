# 以客户端/服务器模式
# CHROMA还可以配置为使用磁盘上的数据库，这对于无法放入内存的较大数据很有用。要在客户端服务器模式下运行CHROMA，请运行DOCKER容器：
'''
docker-compose up -d --build
'''

# 然后更新您的客户端以指向DOCKER容器
import chromadb

from chromadb.config import Settings

client = chromadb.Client(
    Settings(
        chroma_api_impl="rest",
        chroma_server_host="192.168.13.130",
        chroma_server_http_port="8000"
    )
)

# 就是这样！CLIENT-SERVER CHROMA的API将以仅此更改的模式运行。


collection = client.create_collection(
    name="my_collection",
    # embedding_function=emb_fn  # 可选
)
collection = client.get_collection(
    name="my_collection",
    # embedding_function=emb_fn  # 可选
)
collection.add(  # 添加一些文本文档到集合中，CHROMA将存储文本，并自动处理标记化、嵌入和索引
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id3", "id4"]
)
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2
)

print(results)

# collection = client.get_collection(name="test") # Get a collection object from an existing collection, by name. Will raise an exception if it's not found.
# collection = client.get_or_create_collection(name="test") # Get a collection object from an existing collection, by name. If it doesn't exist, create it.
#
# client.delete_collection(name="my_collection") # Delete a collection and all associated embeddings, documents, and metadata. ⚠️ This is destructive and not reversible
#
#
# collection.peek() # returns a list of the first 10 items in the collection
# collection.count() # returns the number of items in the collection
# collection.modify(name="new_name") # Rename the collection
