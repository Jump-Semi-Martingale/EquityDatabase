class Api::EquitiesController < ApplicationController
    skip_before_filter :verify_authenticity_token, only: :create # どうやらこの記述が必要
    
    def create
	equity = Equity.new(create_params)
        equity.save
    end                                                                                                    
    
    private
    def create_params
        params.permit(:t_date,:key_id,:sec_code,:start_price,:end_price,:min_price,:max_price,:trade_volume,:trade_amount)
    end
end
