#!/usr/bin/ruby
require 'date'

if ARGV.length != 2
  puts __FILE__ + " month year"
  exit 1
end

month = ARGV[0].to_i
year  = ARGV[1].to_i

if month < 1 or month > 12
  puts __FILE__ + ": month `" + month.to_s + "' not in range 1..12"
  exit 1
end

if year < 0
  puts __FILE__ + ": year `" + year.to_s + "' not in range 0.."
  exit 1
end

startDate = Date.new(year, month, 1)
if startDate.leap?
  lastDays = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
else
  lastDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
end

print "         [" + month.to_s + " " + year.to_s + "]\n"
print "Sun Mon Tue Wen Thu Fri Sat\n"

startDate.step(startDate + startDate.wday - 1, 1){|date|
  print "    "
}
startDate.step(startDate + lastDays[month - 1] - 1, 1){|date|
  if date.saturday?
    print "%3d" % date.day + "\n"
  else
    print "%3d" % date.day + " "
  end
}

print "\n"
