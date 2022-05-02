import asyncio

async def bar(i):
  print('started', i)
  await asyncio.sleep(1)
  print('finished', i)
  return i

async def not_async(n):
    for i in range(n):
        await bar(i)

async def using_lib(n):
  result = await asyncio.gather(*[bar(i) for i in range(n)])
  return result

# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(using_lib())
# # loop.run_until_complete(function0())
# loop.close()

# print(result)


result = asyncio.run(using_lib(5))
print(result)