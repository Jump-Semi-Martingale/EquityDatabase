#スウィフトに返す
json.array!(@temp) do |js|
   json.(js, :t_date, :end_price)
end
