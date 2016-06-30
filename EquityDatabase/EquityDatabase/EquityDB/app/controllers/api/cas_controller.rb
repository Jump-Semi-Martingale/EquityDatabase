class Api::CasController < ApplicationController
    skip_before_filter :verify_authenticity_token, only: :create # どうやらこの記述が必要

    def create
        ca = Ca.new(create_params)
        ca.save
    end

    private
    def create_params
        params.permit(:key_id,:update_date,:corp_date,:corp_rate,:corp_name)
    end
end
