const cacheName = "AppCache"
const assets = [
  "/",
  "/auth",
  "/revoke"
]

self.addEventListener("install", installEvent => {
    installEvent.waitUntil(
      caches.open(cacheName ).then(cache => {
        cache.addAll(assets)
      })
    )
  })