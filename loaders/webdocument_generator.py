
import asyncio
from crawl4ai import AsyncWebCrawler,CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from loaders.utils import *
import re
from pathlib import Path
from urllib.parse import urlparse


#create dataset from web
async def create_dataset_from_web(sourceName, url):
    print("Source url is:" , url)



   

    #Define Crawler configuration

    config = CrawlerRunConfig(
        page_timeout=30000,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            max_pages=100,
            include_external=False,
        )
    )

    async with AsyncWebCrawler() as crawler:
        try:
            results = await crawler.arun(url=url , config=config)
            print("crawl completed:")
        except Exception as e:
            print("crawler failed.")
            print(e)
            return
        

    #Check if source directory exists
    print("Saving dataset in source directory")
    createDirectoryIfNotPresnt("./sources/web")
    sourcePath=f"./sources/web/{sourceName}"
    createDirectoryIfNotPresnt(sourcePath)

    #Create .md files for results
    print(f"results length: {len(results)}")
        #List of urls in results

    skip_extensions = {
        ".svg", ".png", ".jpg", ".jpeg", ".gif",
        ".ico", ".css", ".js", ".pdf", ".zip"
    }

    for result in results:
        print(f"URL is: {result.url}")

        path = urlparse(result.url).path.lower()
        extension = Path(path).suffix
        if extension in skip_extensions:
            print(f"Skipping resource: {result.url}")
            return
        if result.markdown:
            print(f"Markdown size: {len(result.markdown)}")
        else:
            print("No markdown generated.")
            return
        #print(f"Markdown size: {len(result.markdown)}")
        title=result.metadata["title"]
        print(f"Title is: {title}")
        sourceFilePath=f"{title}.md"
         # Replace invalid Windows characters
        markdownFilePath = re.sub(
        r'[\\/*?:"<>|]',
        "_",
        sourceFilePath
        )
        print(f"md file to Create:{markdownFilePath}")
        create_markdown_file(sourcePath,markdownFilePath,result)