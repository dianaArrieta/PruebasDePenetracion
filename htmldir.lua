local io = require "io"
local http = require("socket.http")
local palabras = {};
print('Ingresa la url')
local url_base = io.read()

print("Buscando directorios ...")

local wordlist = '/usr/share/wordlists/dirb/small.txt'

local file = io.open(wordlist, "r")

local i = 0

for linea in file:lines() do
	palabras[i] = "/" .. linea .. "/"
	i = i + 1 
end

file.close()


for d=0,i-1 do
	url = url_base .. palabras[d]
	local body, code, headers, status = http.request(url)
	if status  == "HTTP/1.1 200 OK" then
		print("DIR => " .. url)
	end
end

