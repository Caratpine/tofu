function wk_recommend(pid,status){
	$.post("/api.php?m=recommend", {recommend: status, pid: pid },function(data){
        alert(data);
        window.location.reload();
    });
}
function wk_share(link,title,tag,user,description){
    $.post("/api.php?m=share", {link: link, title: title,tag:tag,user:user,description:description  },function(data){
        alert(data);
    });
}
function likeNumC(pid){
    var likeNumId = "likeNum-"+pid
	likeNums = $("#"+likeNumId).text()
    likeNums = parseFloat(likeNums) + 1
    $("#"+likeNumId).text(likeNums)
    $.post("/api.php?m=like", {pid: pid},function(data){
        return data
    });
}

function collectC(pid){

    $.post("/api.php?m=collect", {pid: pid},function(data){
        alert(data);
    });
}
