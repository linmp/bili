// 根url
var HOST_URI = 'https://soup.hicaiji.com';
// 获取openid 
var GET_OPENID = '/wx/login?lg_code='
// 更新用户信息 
var UPDATE = '/update'
// 查看鸡汤 
var GET_Soup = '/soup'
// 收藏 需要openid 
var COLLECT = '/collect'
// 取消收藏 需要openid 
var COLLECT_DELETE = '/collect/delete'
// 查看我的收藏 需要openid 
var GET_MY_COLLECT = '/collects?openid='


// 获取openid_token 
function _getOpenid() {
  return HOST_URI + GET_OPENID;
}

// 更新用户信息
function _update() {
  return HOST_URI + UPDATE;
}

// 查看鸡汤
function _getSoup() {
  return HOST_URI + GET_Soup;
}

// 收藏 需要openid 
function _collect() {
  return HOST_URI + COLLECT;
}

// 收藏 需要openid 
function _collectDelete() {
  return HOST_URI + COLLECT_DELETE;
}

// 查看我的收藏 需要openid 
function _getMyCollect() {
  return HOST_URI + GET_MY_COLLECT;
}




module.exports = {
  getOpenid:_getOpenid,
  update:_update,
  getSoup: _getSoup,
  collect: _collect,
  collectDelete: _collectDelete,
  getMyCollect:_getMyCollect
};


