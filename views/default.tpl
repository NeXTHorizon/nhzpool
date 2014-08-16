% include('header.tpl')
        <li class="active"><a href="/">Home</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
        <li><a href="/payouts">Payouts</a></li>
		<li><a href="/unpaid">Unpaid</a></li>
		<li><a href="/paid">Paid</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>
  
  <!-- Begin page content -->
  <div class="container">
  <div class="text-center">
    <div class="page-header">
      <h1>NHZ Forging Pool</h1>
    </div>
    <div class="col-lg-12">
	<h3>Pool Account</h3>    
    <p><strong>{{pa}}</strong></p>
    <p>Pool Fee is {{fee}}%</p>
    <p>Pool Interface is still in testing only raw data is displayed</p>
	</div>
</div>
</div>
</div>
% include('footer.tpl')
