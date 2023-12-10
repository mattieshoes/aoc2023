def recurse(arr)
  if arr.uniq.size == 1 && arr[0].zero?
    return [0,0]
  end
  result = recurse(arr[..-2].zip(arr[1..]).map{|a| a=a[1]-a[0]})
  return [arr[0]-result[0], arr[-1] + result[1]]
end

lines = IO.readlines("inputs/9").map(&:strip)
ans = [0,0]
lines.each { |line|
  fields = line.split(/ /).map(&:to_i)
  ans = [ans, recurse(fields)].transpose.map(&:sum)
}
puts "Part 1: #{ans[1]}"
puts "Part 2: #{ans[0]}"
