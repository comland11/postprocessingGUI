x = linspace(-fov(1) / 2, fov(1) / 2, nPoints(1));
y = linspace(-fov(2) / 2, fov(2) / 2, nPoints(2));
z = linspace(-fov(3) / 2, fov(3) / 2, nPoints(3));

[y, z, x] = meshgrid(y, z, x);

x = x(:);
y = y(:);
z = z(:);

for n = 1:niter
    for t = 1:length(s)
        mt = exp(2 * pi * (-1i * sampled(t, 1) * x + 1i * sampled(t, 2) * y - 1i * sampled(t, 3) * z));

        norm = dot(mt, mt);
        norm1 = mt' * mt;
        delta_t = (-s(t) + mt' .* rho) / norm;

        rho = rho - lbda .* delta_t .* mt';

        fprintf('Iteration %i of %i\n', t, length(s));
    end
end

rho = reshape(rho, nPoints(end:-1:1));

% Save k_space in a .mat file
save('rho.mat', 'rho');
