% include('header.tpl', popular_tags=popular_tags)

<div id="content" class="mui-container-fluid">

	<div class="mui-row">
		<div class="mui-col-sm-10 mui-col-sm-offset-1">

			<div class="mui--text-dark-secondary mui--text-body2"><h1><a href="/">HOME</a> | DAILY PYTHON TIPS ({{ len(tips) }})</h1></div>
			<div class="mui-divider"></div>
			% for tip in tips:
				<div class='tip'>
					<pre>{{ !tip['text'] }}</pre>
					<div class="mui--text-dark-secondary"><strong>{{ tip['favorite_count'] }}</strong> Likes / <strong>{{ tip['retweet_count'] }}</strong> RTs / {{ tip['created_at'] }} / <a href="https://twitter.com/pybites/status/{{ tip['id'] }}" target="_blank">Share</a></div>
				</div>
			% end

		</div>
	</div>

</div>

% include('footer.tpl')
