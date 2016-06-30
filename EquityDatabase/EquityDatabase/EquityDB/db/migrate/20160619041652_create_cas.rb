class CreateCas < ActiveRecord::Migration
  def change
    create_table :cas, id: false  do |t|
      t.datetime :update_date
      t.datetime :corp_date
      t.float :corp_rate
      t.string :corp_name
      t.bigint :key_id
      t.timestamps null: false
    end
  end
end
