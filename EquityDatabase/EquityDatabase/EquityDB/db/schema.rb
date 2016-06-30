# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20160619041652) do

  create_table "cas", id: false, force: :cascade do |t|
    t.datetime "update_date"
    t.datetime "corp_date"
    t.float    "corp_rate",   limit: 24
    t.string   "corp_name",   limit: 255
    t.integer  "key_id",      limit: 8
    t.datetime "created_at",              null: false
    t.datetime "updated_at",              null: false
  end

  create_table "equities", primary_key: "key_id", force: :cascade do |t|
    t.string   "sec_code",     limit: 255
    t.string   "sec_name",     limit: 255
    t.datetime "t_date"
    t.float    "start_price",  limit: 24
    t.float    "end_price",    limit: 24
    t.float    "min_price",    limit: 24
    t.float    "max_price",    limit: 24
    t.float    "trade_volume", limit: 24
    t.float    "trade_amount", limit: 24
    t.datetime "created_at",               null: false
    t.datetime "updated_at",               null: false
  end

end
