require "optparse"
require "zlib"

MESSAGE_KEY = 'SecretMessage'

ProgramConfig = Hash.new
$srcFile = "source.png"
$dstFile = "dst.png"

def handleArguments
  opts = OptionParser.new
  opts.banner = "Usage: png_text -e message srcFile dstFile\n" \
  + "\tpng_text -d srcFile\n" \
  + "\tpng_text -h"
  opts.on("-e MESSAGE", "--encode MESSAGE", "encode MESSAGE into png file"){|message|
    ProgramConfig[:encode] = message
  }
  opts.on("-d", "--decode", "decode message from png file"){|v|
    ProgramConfig[:decode] = true
  }
  opts.on("-v [LEVEL]", "--verbose [LEVEL]", "Show verbose log."){|level|
    if level
      ProgramConfig[:verbose] = level.to_i
    else
      ProgramConfig[:verbose] = 1
    end
  }
  argv = opts.parse(ARGV)

  if ((ProgramConfig[:decode] and ProgramConfig[:encode]) \
      or (!ProgramConfig[:decode] and !ProgramConfig[:encode]))
    puts opts.help
    exit 1
  end

  if argv[0]
    $srcFile = argv[0]
  end

  if argv[1]
    $dstFile = argv[1]
  end
end

def log(message, level = 0)
  if !ProgramConfig[:verbose]
    return
  end
  if level < ProgramConfig[:verbose]
    puts "LOG: " + message
  end
end


PNG_MAGIC_WORD = '89504E470D0A1A0A'
def parsePngMagicWord(src, dst=nil)
  # initial 8 byte : png header (always "89 50 4E 47 0D 0A 1A 0A")

  if !src or src.eof
    if !src
      p __LINE__
    end
    if src.eof
      p __LINE__
    end
    raise "Invalid argument"
  end

  b = src.read(8)
  if b != [PNG_MAGIC_WORD].pack("H*")
    puts b.unpack("H*")
    raise "This file is not PNG file."
  end

  if dst
    dst.write(b)
  end
end

def parsePngChunk(src, dst = nil)
  # 4 byte       : chunk data length => dataLen
  # 4 byte       : chunk type name ('IHDR', 'tEXt', ...)
  # dataLen byte : chunk data
  # 4 byte       : CRC of chuk data

  if !src or src.eof
    raise "Invalid argument"
  end

  dataLen = src.read(4).unpack("N1")[0]
  chkName = src.read(4)
  log "chkName : " + chkName
  chkData = src.read(dataLen)
  crc = src.read(4) # CRC
  if crc.unpack("N1")[0] != Zlib.crc32(chkName + chkData)
    log "  embeded crc    : 0x" + crc.unpack("N1")[0].to_s(16)
    log "  calculated crc : 0x" + Zlib.crc32(chkName + chkData).to_s(16)
    raise "Invalid CRC"
  end

  if chkName == "tEXt"
    log "  tEXt key  : " + chkData.split("\x00")[0]
    log "  tEXt text : " + chkData.split("\x00")[1]
    if chkData.split("\x00")[0] == MESSAGE_KEY
      message =  chkData.split("\x00")[1]
    end
  end

  if dst
    dst.write([dataLen].pack("N1"))
    dst.write(chkName)
    dst.write(chkData)
    dst.write(crc)
  end

  return message
end

def addPngTextChunk(dst, message)
  dataLen = MESSAGE_KEY.bytesize + 1 + message.bytesize
  chunkData = MESSAGE_KEY + [0].pack("C1") + message
  crc = Zlib.crc32("tEXt" + chunkData, 0)
  dst.write([dataLen].pack("N1")) # Chunk Data Length
  dst.write("tEXt")               # Chunk Type
  dst.write(chunkData)            # Chunk Data
  dst.write([crc].pack("N1"))     # CRC 4byte

  log "chkName : tEXt"
  log "  tEXt key  : " + MESSAGE_KEY
  log "  tEXt text : " + message
  log "  crc       : 0x" + crc.to_s(16)
end

def encodeMessage(message)
  open($srcFile, "rb") {|src|
    open($dstFile, "wb") {|dst|
      parsePngMagicWord(src, dst)

      # IHDR
      parsePngChunk(src, dst)

      # Secret Message
      addPngTextChunk(dst, message)

      # copy rest data
      dst.write(src.read)
    }
  }
end

def decodeMessage
  messages = []
  open($srcFile, "rb") {|src|

    parsePngMagicWord(src)

    until src.eof
      message = parsePngChunk(src)
      if message
        messages << message
      end
    end
  }

  return messages
end


handleArguments

if ProgramConfig[:encode]
  message = ProgramConfig[:encode]
  encodeMessage(message)
  exit
end

if ProgramConfig[:decode]
  message = decodeMessage()
  if message.length > 0
    puts "Secret Message is " + message.to_s
  else
    puts "Secret Message is not found..."
  end
  exit
end
