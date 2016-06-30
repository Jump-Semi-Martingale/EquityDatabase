class Api::SwiftdisplaysController < ApplicationController
    skip_before_filter :verify_authenticity_token, only: :create # どうやらこの記述が必要

    #DBから持ってくる
    def create
        from_date = params[:from_date]
        to_date = params[:to_date]
        sec_code = params[:sec_code]
        start_key_id = sec_code + from_date
        end_key_id = sec_code + to_date
        start_key_id = start_key_id.to_i #10進数の数値に変換
        end_key_id = end_key_id.to_i

        #SQL文の直接実行
        @temp = Equity.find_by_sql(['select key_id, t_date, end_price from equities where key_id >= :start_key_id and key_id <= :end_key_id', {:start_key_id => start_key_id, :end_key_id => end_key_id}])
        #print(@temp)

#        i = 0
#	while i < @temp.length 
#	    @temp[i][:t_date] = @temp[i][:t_date].strftime("%Y年%m月%d日")
#	#    print(@temp[i][:end_price]) 
#	i+=1
#	end
        #render json: @temp
    end
end
