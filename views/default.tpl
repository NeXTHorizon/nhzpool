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
<div class="row">
  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
  <h4><strong>Pool Account:</strong> {{pa}}</h4>
  <p></p>
    <p>Pool Fee is {{fee}}%</p>
    <p>Pool Interface is still in testing only raw data is displayed</p>
  </div> 
</div>
<div class="row">
  <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
  <h3>Active Leased Accounts</h3>
  <div class="table-responsive">
<table class="table table-striped table-bordered table-condensed table-hover">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>
</div>
  </div>
  <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
  <h3>Last Blocks Found</h3>
    <div class="table-responsive">
<table class="table table-striped table-bordered table-condensed table-hover">
%for row in blocks:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>
</div>
  </div>
  </div>
</div>
</div>
</div>
</div>
% include('footer.tpl')
