<?php 
if($compression == true){
	function sanitize_output($buffer) {
		$search = array(
			'/\>[^\S ]+/s',     // strip whitespaces after tags, except space
			'/[^\S ]+\</s',     // strip whitespaces before tags, except space
			'/(\s)+/s',         // shorten multiple whitespace sequences
			'/<!--(.|\s)*?-->/' // Remove HTML comments
		);
		$replace = array(
			'>',
			'<',
			'\\1',
			''
		);
		$buffer = preg_replace($search, $replace, $buffer);
		return $buffer;
	}
	ob_start("sanitize_output");
}
@session_start();
error_reporting(1);
set_time_limit(727379969012);
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=31536000");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
header('Access-Control-Allow-Origin: *');  
/* Random number for file version names */
function randomString($length = 10) {
	$str = "";
	$characters = array_merge(range('A','Z'), range('a','z'), range('0','9'));
	$max = count($characters) - 1;
	for ($i = 0; $i < $length; $i++) {
		$rand = mt_rand(0, $max);
		$str .= $characters[$rand];
	}
	return $str;
};
/* Mobile Detect PHP Script */
require_once "includes/lib/mobile_detect.php";
$detect = new Mobile_Detect;
include_once("constants.php");
extract($_GET);
extract($_POST);
extract($_COOKIE);
extract($_REQUEST);
extract($_SESSION);
?>