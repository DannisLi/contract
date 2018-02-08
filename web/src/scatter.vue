<template scoped>
	<div :id="field" style="width:1200px;height:650px;margin:0 auto;"></div>
</template>

<script scoped>
	import echarts from 'echarts';
	import $ from 'jquery';
	
	function min(arr) {
		var res = arr[0];
		for (var i=1; i<arr.length; i++) {
			if (res > arr[i]) {
				res = arr[i];
			}
		}
		return res;
	}
	
	function max(arr) {
		var res = arr[0];
		for (var i=0; i<arr.length; i++) {
			if (res < arr[i]) {
				res = arr[i];
			}
		}
		return res;
	}
	
	export default {
		props: ['field', 'vari', 'deli'],
		data () {
			return {
				chart: null,
				option: {
					title: {
						text: this.field,
					},
					xAxis: {
						name: 'T-1日',
						type: 'value',
						min: null,
						max: null,
					},
					yAxis: {
						name: 'T日',
						type: 'value',
						min: null,
						max: null,
					},
					visualMap: [{
						type: 'continuous',
						calculable: true,
						dimension: 2,
						min: null,
						max: null,
					}],
					series: [{
						type: 'scatter',
						data: null,
						markLine: {
							animation: false,
							label: {
								normal: {
									formatter: '',
									textStyle: {
										align: 'right',
										fontSize: 18,
									}
								}
							},
							lineStyle: {
								normal: {
									type: 'solid'
								}
							},
							data: [[{
								coord: null,
								symbol: 'none',
							}, {
								coord: null,
								symbol: 'none',
							}]],
						},
					}],
				},
			}
		},
		methods: {
			draw () {
				console.log(this.vari, this.deli);
				var _this = this;
				$.get('http://127.0.0.1:8888/single_diff/', {field:_this.field, vari:_this.vari, deli:_this.deli}, function (data) {
					data = JSON.parse(data);
					
					if (data===null) {
						_this.chart.clear();
						return ;
					}
					
					var series = data.series;
					var opt = _this.option;
					opt.series[0].data = new Array();
					for (var i=1; i<series.length; i++) {
						opt.series[0].data.push([series[i-1], series[i], i]);
					}
					opt.visualMap[0].min = 1;
					opt.visualMap[0].max = series.length-1;
					
					var _min = Math.floor(min(series) * 0.9);
					opt.xAxis.min = _min;
					opt.yAxis.min = _min;
					
					var _max = Math.ceil(max(series) * 1.05);
					opt.xAxis.max = _max;
					opt.yAxis.max = _max;
					
					var beta0 = Math.round(data.beta0*100) / 100;
					var beta1 = Math.round(data.beta1*100) / 100;
					
					if (beta0+_min*beta1 < _min) {
						opt.series[0].markLine.data[0][0].coord = [(_min-beta0)/beta1, _min];
					} else {
						opt.series[0].markLine.data[0][0].coord = [_min, beta0+_min*beta1];
					}
					if (beta0+_max*beta1 > _max) {
						opt.series[0].markLine.data[0][1].coord = [(_max-beta0)/beta1, _max];
					} else {
						opt.series[0].markLine.data[0][1].coord = [_max, beta0+_max*beta1];
					}
					opt.series[0].markLine.label.normal.formatter = 'y = ' + beta0 + ' + ' + beta1 + ' * x';
					
					_this.chart.setOption(opt);
				});
			},
		},
		watch: {
			vari: 'draw',
			deli: 'draw',
		},
		mounted () {
			this.chart = echarts.init(document.getElementById(this.field));
			this.draw();
		},
	}
</script>