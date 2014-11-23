% include('header.tpl')
<li><a href="/">Home</a></li>
        <li class="active"><a href="/getting_started">Getting Started</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
        <li class="dropdown">
          <a href="/payouts" class="dropdown-toggle" data-toggle="dropdown">
            Payout Data<b class="caret"></b>
          </a>
          <ul class="dropdown-menu">
            <li><a href="/payouts">Payouts</a></li>
			<li><a href="/unpaid">Unpaid</a></li>
			<li><a href="/paid">Paid</a></li>        
          </ul>
        </li>
        </ul>
        <div class="col-sm-3 col-md-3 pull-right">
            <form class="navbar-form" action="/user" role="form" method="post">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Account Name" name="username">
                    <div class="input-group-btn">
                        <button class="btn btn-default" type="submit"><i class="glyphicon glyphicon-search"></i></button>
                    </div>
                </div>
            </form>
         </div>
      </div><!--/.nav-collapse -->
    </div>
  </div>
  
<div class="container">
  
  <div class="text-center">
  	<div class="page-header">
	<h1>Getting Started:</h1>
  	</div>
<div class="row">
    <div class="text-center">
        <p>Thanks to Nick of Cryptoπa for this excellent tutorial on leasing your balance to our forge pool.</p>
        <iframe width="640" height="480" src="//www.youtube.com/embed/QEkRr0OaSZA" frameborder="0" allowfullscreen></iframe>
    </div>
</div>
</div>  
</div>
</div>
% include('footer.tpl')