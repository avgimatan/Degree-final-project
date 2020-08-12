const mongoose     = require('mongoose');
const mongoosastic = require('mongoosastic');

mongoose.connect('mongodb://localhost:27017/landingZoneDB');

var DNMAvengers_tbSchema = new mongoose.Schema({ 
	crawl_date:{type:String, es_indexed:true}
	,views:{type:String, es_indexed:true}
	,replies:{type:String, es_indexed:true}
	,title:{type: String, es_indexed:true}
	,comments: [{joined_date:{type:String, es_indexed:true} , comment_date:{type:String, es_indexed:true}
	    ,comment_body:{type:String, es_indexed:true}, user_link:{type:String, es_indexed:true}
	    ,posts_count:{type:String, es_indexed:true}, user_name:{type:String, es_indexed:true}
	    ,urls_regex: [{type:String, es_indexed:true}], bitcoin_regex: [{type:String, es_indexed:true}]
	    , emails_regex: [{type:String, es_indexed:true}]}]
	,link:{type: String, es_indexed:true}
	,forum_title:{type: String, es_indexed:true}
	,avatar_details: {avatar_name:{type: String, es_indexed:true} ,avatar_pass:{type: String, es_indexed:true}
	    ,avatar_user:{type:String, es_indexed:true}, avatar_email:{type: String, es_indexed:true} }
}, {versionKey: false});

DNMAvengers_tbSchema.plugin(mongoosastic);

var dnmavengers = mongoose.model('dnmavengers', DNMAvengers_tbSchema)
  , count = 0;

dnmavengers.createMapping({ },function(err, mapping){ });

var stream = dnmavengers.synchronize({}, {saveOnSynchronize: true})

stream.on('data', function(err, doc){
  count++;
});
stream.on('close', function(){
  console.log('indexed ' + count + ' documents!');
});

stream.on('error', function(err){
  console.log(err);
});
