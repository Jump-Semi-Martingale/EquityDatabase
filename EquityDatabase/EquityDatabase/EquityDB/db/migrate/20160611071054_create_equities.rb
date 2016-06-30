class CreateEquities < ActiveRecord::Migration
  def change
    create_table :equities, id: false do |t|
      t.string :sec_code
      t.string :sec_name
      t.datetime :t_date
      t.float :start_price
      t.float :end_price
      t.float :min_price
      t.float :max_price
      t.float :trade_volume
      t.float :trade_amount	
      t.bigint :key_id
      t.timestamps null: false
    end
  end
end
